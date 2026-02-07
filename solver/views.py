import os
from django.shortcuts import render
from solver.models import EngineeringProblem, VerificationAttempt
from .auditor_logic.auditor import Auditor
from .auditor_logic.proposer import Proposer
from .auditor_logic.skeptic import Skeptic
from django.views.decorators.csrf import csrf_protect
from django.db.models import Count, Q, Avg
import json

@csrf_protect
def index(request):
    return render(request, 'solver/index.html')


@csrf_protect
def solve_engineering_view(request):
    # GET: Just show the home page with the math-field
    if request.method == "GET":
        return render(request, "solver/index.html")

    # POST: Process the problem and redirect to results
    if request.method == "POST":
        # In a standard form POST, query comes from request.POST
        query = request.POST.get("query")

        if not query:
            return render(request, "solver/index.html", {"error": "Query cannot be empty"})

        # 1. Initialize Multi-Agent System
        api_keys = {}
        for i in range(1, 4):
            api_keys[f"GROQ_API_KEY{i}"] = os.getenv(f"GROQ_API_KEY{i}")
        
        for key, value in api_keys.items():
            proposer = Proposer(api_key=value)
            skeptic = Skeptic(api_key=value)
            auditor = Auditor(proposer, skeptic, max_attempts=2)

            # 2. Run the Logic Loop (Synchronous)
            try:
                history = auditor.process_query(query)
            except Exception as e:
                if key == "GROQ_API_KEY3":
                    return render(request, "solver/index.html", {"error": f"Error processing query: {str(e)}"})
                else:
                    continue
            break
        final_result = history[-1]

        # 3. Persistent Storage (Keep this for your ENSAM Analytics)
        problem_record = EngineeringProblem.objects.create(
            prompt=query,
            category=final_result.get("category", "General"),
            final_solution=final_result.get("proposed_solution"),
            verification_status=final_result.get("final_status"),
            total_attempts=len(history)
        )
        
        for attempt in history:
            VerificationAttempt.objects.create(
                problem=problem_record,
                sympy_code=attempt.get("code", ""),
                code_status=attempt.get("symbolic_passed", False),
                code_error_message=attempt.get("error_msg", ""),
                LLM_status=attempt.get("semantic_status", False),
                LLM_affirmation=attempt.get("affirmation", ""),
                LLM_corrections=attempt.get("corrections", ""),
                full_LLM_output=attempt.get("full_LLM_output", ""),
                LLM_feedback=attempt.get("LLM_feedback", ""),
                is_sympy_error=attempt.get("is_sympy_error", False)
            )

        # 4. Render the Result Page directly
        # We pass 'history' and 'final' so the template can iterate over them
        return render(request, "solver/result.html", {
            "query": query,
            "final": final_result,
            "history": history
        })

def analytics_dashboard(request):
    # Overall Metrics
    total_problems = EngineeringProblem.objects.count()
    overall_verified = EngineeringProblem.objects.filter(verification_status="VERIFIED").count()
    
    # Detailed Category Stats
    categories = list(EngineeringProblem.objects.values_list('category', flat=True).distinct())
    study_data = []
    
    # Chart Data Lists
    v_data, sym_data, sem_data, fail_data = [], [], [], []

    for cat in categories:
        qs = EngineeringProblem.objects.filter(category=cat)
        cat_total = qs.count()
        
        # State Counts
        v = qs.filter(verification_status='VERIFIED').count()
        sym = qs.filter(verification_status='SYMBOLIC_ONLY_PASS').count()
        sem = qs.filter(verification_status='SEMANTIC_ONLY_PASS').count()
        f = qs.filter(verification_status='BOTH_FAILURE').count()

        # Append to Table Data
        study_data.append({
            'category': cat,
            'total': cat_total,
            'avg_attempts': qs.aggregate(Avg('total_attempts'))['total_attempts__avg'] or 0,
            'hallucination_rate': (sem / cat_total * 100) if cat_total > 0 else 0
        })

        # Append to Chart Data (%)
        if cat_total > 0:
            v_data.append(round((v / cat_total) * 100, 1))
            sym_data.append(round((sym / cat_total) * 100, 1))
            sem_data.append(round((sem / cat_total) * 100, 1))
            fail_data.append(round((f / cat_total) * 100, 1))

    return render(request, "solver/analytics.html", {
        "total_problems": total_problems,
        "verified_rate": (overall_verified / total_problems * 100) if total_problems > 0 else 0,
        "category_stats": study_data,
        "chart_categories": json.dumps(categories),
        "v_data": json.dumps(v_data),
        "sym_data": json.dumps(sym_data),
        "sem_data": json.dumps(sem_data),
        "fail_data": json.dumps(fail_data),
    })