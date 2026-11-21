# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`

**Created**: [DATE]

**Status**: Draft

**Input**: User description: "$ARGUMENTS"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
- **FR-002**: System MUST [specific capability, e.g., "validate email addresses"]
- **FR-003**: Users MUST be able to [key interaction, e.g., "reset their password"]
- **FR-004**: System MUST [data requirement, e.g., "persist user preferences"]
- **FR-005**: System MUST [behavior, e.g., "log all security events"]

*Example of marking unclear requirements:*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- **FR-007**: System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Constitutional Alignment *(mandatory)*

<!--
  ACTION REQUIRED: Replace with concrete OraDiag SDD alignment. Every item must
  be specific to this feature and traceable to the constitution and rector docs.
-->

### Roadmap and Scope

- **Roadmap grouping**: [Spec 003-012 de `docs/ROADMAP.md`; 001 y 002 son históricas]
- **Rector docs used**: [docs/... files that govern this feature]
- **Out of scope**: [Explicitly state future specs and prohibited scope not
  included]
- **Deviation status**: [None, or `propuesta de desviación` with human
  authorization required]

### Oracle Sources, Grants and Licensing

<!--
  Una fila por vista, paquete o fuente de plataforma que use la spec.
  Licencia: none | diagnostic_pack | tuning_pack. Fuente: sql | licensed | platform | lab.
  Validar la columna Licencia contra "Database Licensing Information" de cada versión soportada.
-->

| Vista / fuente | Fuente | Licencia | Grant normal | Grant en RDS | Versión mínima |
|---|---|---|---|---|---|
| [V$SESSION] | [sql] | [none] | [GRANT SELECT ON V_$SESSION TO oradiag] | [EXEC rdsadmin.rdsadmin_util.grant_sys_object('V_$SESSION','ORADIAG','SELECT')] | [19c] |

- **Read-only**: [Confirm only SELECT; no DML/DDL, ALTER SYSTEM, server files or
  state-changing procedures]
- **Platform independence**: [Confirm core sources are SQL-only; list any
  platform adapter used and what becomes `not_evaluated` without it]
- **Licensed sources**: [None, or list with `diagnostic_pack`/`tuning_pack`
  declaration and `control_management_pack_access` check]
- **Query cost**: [Time window and filters that bound each query in production]

### RCA and Evidence Rules

- **Incident/RCA focus**: [How this supports incident diagnosis instead of
  health check/capacity planning]
- **Evidence required**: [Positive evidence, negative evidence and limitations]
- **Symptom handling**: [How symptoms prioritize but do not decide causality]
- **Causal roles**: [Which roles can be emitted and under what evidence]
- **Causal correlation**: [Causal rules or evidence chains; how the incident
  window decides primary vs incidental; never by severity alone]
- **Visible OK reviews**: [OK results that must remain visible]
- **Causal domains**: [Approved domains used; explain Datos boundary if
  applicable]

### Safety, Data and Error Boundaries

- **No business data**: [Confirm no business tables, functional data or
  application-data meaning are queried, modeled or inferred; SQL text and bind
  values treated as sensitive and masked in reports]
- **Failures/timeouts**: [How errors, timeouts, missing permissions and missing
  layers become limitations or non-evaluated reviews]
- **Security/minimum privileges**: [Secrets handling and minimum technical
  privileges]
- **Recommendations**: [Risk, prerequisites and human validation requirements]
- **Evidence Payload/format**: [JSON contract/versioning/validation; YAML only
  for human lab scenarios if applicable]
- **Language**: [Spanish human documentation, reports and principal messages]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]

## Assumptions

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right assumptions based on reasonable defaults
  chosen when the feature description did not specify certain details.
-->

- [Assumption about target users, e.g., "Users have stable internet connectivity"]
- [Assumption about scope boundaries, e.g., "Mobile support is out of scope for v1"]
- [Assumption about data/environment, e.g., "Existing authentication system will be reused"]
- [Dependency on existing system/service, e.g., "Requires access to the existing user profile API"]
