from typing import Any

from oradiag.models import DiagnosticResult, EvidencePayload


FORBIDDEN_BUSINESS_FIELDS = {
    "account_number",
    "business_data",
    "business_key",
    "customer_id",
    "document_number",
    "functional_data",
    "invoice_id",
    "order_id",
    "row_id",
    "table_name",
    "transaction_id",
}


EVIDENCE_TECHNICAL_FIELDS = {
    "check_id",
    "id",
    "observations",
    "profile",
    "scenario",
    "schema_version",
    "target_id",
}

DIAGNOSTIC_TECHNICAL_FIELDS = {
    "assessment",
    "evidence_ids",
    "findings",
    "primary_cause_id",
    "scenario",
    "schema_version",
}


def collect_schema_property_names(schema: dict[str, Any]) -> set[str]:
    names: set[str] = set()

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            properties = value.get("properties")
            if isinstance(properties, dict):
                names.update(properties)
            for nested in value.values():
                walk(nested)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(schema)
    return names


def test_evidence_payload_contract_does_not_require_business_data_fields() -> None:
    property_names = collect_schema_property_names(EvidencePayload.model_json_schema())

    assert EVIDENCE_TECHNICAL_FIELDS.issubset(property_names)
    assert FORBIDDEN_BUSINESS_FIELDS.isdisjoint(property_names)


def test_diagnostic_result_contract_does_not_require_business_data_fields() -> None:
    property_names = collect_schema_property_names(DiagnosticResult.model_json_schema())

    assert DIAGNOSTIC_TECHNICAL_FIELDS.issubset(property_names)
    assert FORBIDDEN_BUSINESS_FIELDS.isdisjoint(property_names)
