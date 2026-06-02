from fastapi import APIRouter, HTTPException

router = APIRouter()


mock_reports = [
    {
        "report_id": "REP-001",
        "incident_id": "ALT-001",
        "title": "Brute Force Attack Investigation",

        "summary": (
            "Multiple failed login attempts were detected "
            "followed by a successful login and PowerShell execution."
        ),

        "severity": "Critical",

        "mitre_mapping": [
            "T1110",
            "T1059"
        ],

        "alternative_hypotheses": [
            {
                "name": "Password Spraying",
                "confidence": 12
            },
            {
                "name": "Misconfigured Application",
                "confidence": 6
            }
        ],

        "recommended_actions": [
            "Block source IP",
            "Reset account credentials",
            "Enable MFA",
            "Review PowerShell logs"
        ]
    }
]


@router.get("/reports")
def get_reports():

    return {
        "status": "success",
        "count": len(mock_reports),
        "reports": mock_reports
    }


@router.get("/reports/{report_id}")
def get_report(report_id: str):

    for report in mock_reports:
        if report["report_id"] == report_id:
            return {
                "status": "success",
                "report": report
            }

    raise HTTPException(
        status_code=404,
        detail="Report not found"
    )