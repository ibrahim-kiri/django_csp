"""
CSP violation report endpoint.
The browser POSTs JSON here whenever it detects a CSP violation (requires report-uri in SECURE_CSP_REPORT_ONLY or SECURE_CSP).
"""
import json
import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

logger = logging.getLogger("csp")

@csrf_exempt
@require_POST
def csp_report(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        report = data.get("csp-report", {})
        logger.warning(
            "\n"
            "------------------------------------\n"
            "CSP VIOLATION REPORT\n"
            "------------------------------------\n"
            "Page: %s\n"
            "Directive: %s\n"
            "Blocked: %s\n"
            "Source: %s line %s\n"
            "------------------------------------",
            report.get("document-uri", "-"),
            report.get("violated-directive", "-"),
            report.get("blocked-uri", "-"),
            report.get("source-file", "-"),
            report.get("line-number", "-"),
        )
    except Exception:
        pass
    return HttpResponse(status=204)