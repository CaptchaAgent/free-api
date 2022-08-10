from django.shortcuts import render
from django.http import HttpResponse
import json

from .solver import build_solver


def docs(request):
    return HttpResponse("Hello, world. You're at the challenger docs.")


def api(request, solver_name: str):
    try:
        solver_name = solver_name.lower()

        solver = build_solver(solver_name)

        challenge = request.POST.get("challenge")
        if challenge is None:
            raise ValueError("challenge is required")

        prompt = request.POST.get("prompt")
        if prompt is None:
            raise ValueError("prompt is required")

        content = request.FILES.getlist("img")
        if content is None:
            raise ValueError("content is required")

        lang = request.POST.get("lang")
        if lang is None:
            lang = "en"

        result = solver.solve(
            challenge=challenge, prompt=prompt, content=content, lang=lang
        )

        return HttpResponse(
            json.dumps({"result": result}),
            content_type="application/json",
            status=200,
        )

    except ValueError as e:
        return HttpResponse(
            json.dumps({"result": "error", "message": str(e)}),
            status=400,
            content_type="application/json",
        )
    except Exception as e:
        return HttpResponse(
            json.dumps({"result": "error", "message": str(e)}),
            status=500,
            content_type="application/json",
        )
