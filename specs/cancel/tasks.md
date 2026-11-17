# Tasks: Cancel a reservation

Status: approved
<!-- In this course the agent drafts the tasks (see the organizer role) and a human approves them. -->

| Task | Requirements | Files | Test first |
|------|--------------|-------|------------|
| T1 Return 404 for missing or foreign reservations | REQ-03 | `app/features/cancel.py` | `test_req_03_*` |
| T2 Return 409 when status is not CONFIRMED | REQ-04 | `app/features/cancel.py` | `test_req_04_*` |
| T3 Return 409 when less than 2 hours remain | REQ-02 | `app/features/cancel.py` | `test_req_02_*` |
| T4 Set CANCELLED and return 200 | REQ-01 | `app/features/cancel.py` | `test_req_01_*` |

Order matters: the checks run from "is it even mine" to "is it too late", then the change is made.
