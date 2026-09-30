# Software Engineering Submissions

## Student Details

- **Name:** Akshay V Gudur
- **SRN:** PES1UG24CS047

## Repository Structure

```text
SE-submissions/
├── README.md
├── LAB 1/
│   ├── Requirements_Table_Lab_1.docx
│   ├── Use_Case_Flow_Run_Daily_Audit.docx
│   └── UML_use_case_diagram_LAB1.pdf
├── LAB 2/
│   └── Lab2_Jira_EPICs_Burndown_Charts.pdf
├── LAB 3/
│   ├── PES1UG24CS047_Component_Diagram.pdf
│   └── PES1UG24CS047_Architecture_Justification.pdf
└── LAB 4/
    ├── README.md
    ├── Chat_History.pdf
    ├── Chat_Link.txt
    ├── Implementation_Notes.md
    ├── target-aim-trainer/
    │   ├── README.md
    │   ├── main.py
    │   ├── requirements.txt
    │   ├── game/
    │   │   ├── game_engine.py
    │   │   ├── target.py
    │   │   └── sound.py
    │   └── tests/
    │       ├── test_engine.py
    │       ├── test_target.py
    │       └── test_sound.py
    └── videos/
        ├── README.md
        ├── before.mp4
        ├── after.mp4
        └── push_recording.mp4
```

## Lab 1

**Problem Statement #47 — Domain & SSL Certificate Expiry Alert System**

The `LAB 1` folder contains the requirements table, use-case flow, and UML use-case diagram submission.

### Deliverables

1. Requirements Table — Word document
2. Use-Case Flow — Word document
3. UML Use-Case Diagram — PDF

## Lab 2

**Agile Backlog Creation & Sprint Simulation in Jira — Domain & SSL Certificate Expiry Alert System**

The `LAB 2` folder contains the Jira-based backlog and sprint simulation report. The submission documents 5 epics, 10 user stories, and 50 total story points across 2 completed sprints.

### Deliverables

1. Project basis and functional requirements mapping
2. Epics and user stories with priorities and story-point estimates
3. Detailed user stories and estimation
4. Jira backlog evidence
5. Sprint 1 evidence — 21 story points
6. Sprint 2 evidence — 29 story points
7. Sprint 2 burndown chart and interpretation
8. Reflection on estimation, prioritization, sprint alignment, and team capacity

## Lab 3

**Component Modelling & Architectural Pattern Selection — Domain & SSL Certificate Expiry Alert System**

The `LAB 3` folder contains the UML component diagram and a one-page architecture justification. The selected **Layered Architecture** separates presentation, application logic, and infrastructure.

The diagram shows 8 components with provided and required interfaces, covering daily TLS and WHOIS checks, endpoint management, stored audit results, expiry alerts, notifications, and acknowledgement-based escalation control.

### Deliverables

1. UML Component Diagram — PDF
3. One-page Architecture Justification — PDF

### Architecture Justification

- Comparison of Layered, Microservices, and Client-Server architectures
- Selected architecture and two scenario-specific reasons
- Security advantage through controlled access and protected credentials
- Performance benefit through bounded asynchronous monitoring

The design supports the target of checking 1,000 endpoints in under 3 minutes; benchmarking is required to verify this target.

## Lab 4

**VibeCoding - Target Aim Trainer (assigned project 47)**

The [LAB 4 submission](LAB%204/README.md) contains the completed Python/Pygame
aim trainer, gameplay and push recordings, chat evidence, implementation notes,
and regression tests.

### Implemented changes

1. **Collision fix:** hit detection matches the target's visible shrinking radius.
2. **Game-over screen:** displays final score, accuracy, hits, and misses.
3. **Replay and difficulty:** Easy, Medium, and Hard can be selected after a round.
4. **Sound feedback:** distinct effects for hits, missed clicks, target timeouts,
   and round completion; M toggles mute.

One debugging commit and three separate feature commits implement the four
assigned tasks. All four have been published to this repository and the
[personal game repository](https://github.com/sickDoughnut-007/47_target-aim-trainer).

### Submitted evidence

- [Before gameplay recording](LAB%204/videos/before.mp4)
- [After gameplay recording](LAB%204/videos/after.mp4)
- [Recorded push and GitHub verification](LAB%204/videos/push_recording.mp4)
- [Chat history PDF](LAB%204/Chat_History.pdf) and [shared chat link](LAB%204/Chat_Link.txt)
- [Implementation notes](LAB%204/Implementation_Notes.md)

The implementation passed 14 automated checks and rendered-screen review.
See the Lab 4 README for setup, controls, and timing details.
