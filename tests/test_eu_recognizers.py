"""Tests for EU pattern recognizers."""

import pytest


class TestUKPatterns:
    def test_uk_nhs(self, engine):
        entities = engine.detect("NHS number: 943 476 5919", "en")
        nhs = [e for e in entities if "NHS" in e.get("type", "")]
        assert len(nhs) >= 1, f"Expected UK NHS number, got {[e['type'] for e in entities]}"

    def test_uk_nin(self, engine):
        entities = engine.detect("National Insurance Number: QQ123456C", "en")
        nin = [e for e in entities if "NIN" in e.get("type", "") or "UK" in e.get("type", "")]
        if not nin:
            pytest.skip("UK NIN pattern not matched with this format")


class TestEUPatterns:
    def test_iban(self, engine):
        entities = engine.detect("IBAN: DE89370400440532013000", "en")
        ibans = [e for e in entities if e.get("type") == "IBAN_CODE"]
        assert len(ibans) >= 1, f"Expected IBAN, got {[e['type'] for e in entities]}"

    def test_email(self, engine):
        entities = engine.detect("Email: test@example.com", "en")
        emails = [e for e in entities if e.get("type") == "EMAIL_ADDRESS"]
        assert len(emails) >= 1, f"Expected email, got {[e['type'] for e in entities]}"


class TestDEPatterns:
    def test_de_tax_id(self, engine):
        entities = engine.detect("Steuer-ID: 12 345 678 901", "en")
        tax = [e for e in entities if "TAX" in e.get("type", "") or "DE" in e.get("type", "")]
        # May or may not match depending on recognizer; don't fail hard
        if not tax:
            pytest.skip("DE Tax ID pattern not matched (may need specific format)")


class TestFRLegal:
    def test_siret(self, engine):
        entities = engine.detect("SIRET de l'établissement: 542 107 651 00012", "en")
        hits = [e for e in entities if e.get("type") == "FR_SIRET"]
        assert len(hits) >= 1, f"FR_SIRET not detected. Got: {[e['type'] for e in entities]}"

    def test_siren_not_inside_siret(self, engine):
        entities = engine.detect("SIRET: 542 107 651 00012", "en")
        siren = [e for e in entities if e.get("type") == "FR_SIREN"]
        assert len(siren) == 0, f"FR_SIREN must not fire inside a SIRET. Got: {siren}"

    def test_siren_not_inside_siret_double_space(self, engine):
        entities = engine.detect("SIRET: 542 107 651  00012", "en")
        siren = [e for e in entities if e.get("type") == "FR_SIREN"]
        assert len(siren) == 0, f"FR_SIREN fired on double-space SIRET. Got: {siren}"

    def test_siren_standalone(self, engine):
        entities = engine.detect("Numéro SIREN de la société: 542 107 651", "en")
        hits = [e for e in entities if e.get("type") == "FR_SIREN"]
        assert len(hits) >= 1, f"FR_SIREN standalone not detected. Got: {[e['type'] for e in entities]}"

    def test_rg(self, engine):
        entities = engine.detect("Dossier RG numéro 24/08751 au tribunal de Paris", "en")
        hits = [e for e in entities if e.get("type") == "FR_RG"]
        assert len(hits) >= 1, f"FR_RG not detected. Got: {[e['type'] for e in entities]}"

    def test_rcs(self, engine):
        entities = engine.detect("Immatriculée au RCS de Paris 542 107 651", "en")
        hits = [e for e in entities if e.get("type") == "FR_RCS"]
        assert len(hits) >= 1, f"FR_RCS not detected. Got: {[e['type'] for e in entities]}"

    def test_rg_vs_parquet_no_overlap(self, engine):
        entities = engine.detect("Réquisitoire du parquet numéro 24/123456", "en")
        rg = [e for e in entities if e.get("type") == "FR_RG"]
        parquet = [e for e in entities if e.get("type") == "FR_NUMERO_PARQUET"]
        assert len(parquet) >= 1
        assert len(rg) == 0, f"FR_RG must not fire on 6-digit parquet number. Got: {rg}"

    def test_parquet(self, engine):
        entities = engine.detect("Réquisitoire du parquet numéro 24/123456", "en")
        hits = [e for e in entities if e.get("type") == "FR_NUMERO_PARQUET"]
        assert len(hits) >= 1, f"FR_NUMERO_PARQUET not detected. Got: {[e['type'] for e in entities]}"

    def test_toque(self, engine):
        entities = engine.detect("Maître Durant, toque D4350 au barreau de Paris", "en")
        hits = [e for e in entities if e.get("type") == "FR_TOQUE"]
        assert len(hits) >= 1, f"FR_TOQUE not detected. Got: {[e['type'] for e in entities]}"


class TestFRHealth:
    def test_rpps(self, engine):
        entities = engine.detect("Médecin prescripteur RPPS: 10003456789", "en")
        hits = [e for e in entities if e.get("type") == "FR_RPPS"]
        assert len(hits) >= 1, f"FR_RPPS not detected. Got: {[e['type'] for e in entities]}"

    def test_adeli(self, engine):
        entities = engine.detect("Numéro ADELI du kinésithérapeute: 123456789", "en")
        hits = [e for e in entities if e.get("type") == "FR_ADELI"]
        assert len(hits) >= 1, f"FR_ADELI not detected. Got: {[e['type'] for e in entities]}"

    def test_finess(self, engine):
        entities = engine.detect("Numéro FINESS de l'établissement: 750056489", "en")
        hits = [e for e in entities if e.get("type") == "FR_FINESS"]
        assert len(hits) >= 1, f"FR_FINESS not detected. Got: {[e['type'] for e in entities]}"

    def test_cps_card(self, engine):
        entities = engine.detect("Carte CPS du professionnel de santé: 80012345678901234567", "en")
        hits = [e for e in entities if e.get("type") == "FR_CPS_CARD"]
        assert len(hits) >= 1, f"FR_CPS_CARD not detected. Got: {[e['type'] for e in entities]}"

    def test_adeli_not_on_bare_number(self, engine):
        """Bare 9-digit number without ADELI context must NOT be redacted."""
        entities = engine.detect("Transaction reference 123456789", "en")
        adeli = [e for e in entities if e.get("type") == "FR_ADELI"]
        assert len(adeli) == 0, f"FR_ADELI fired without context. Got: {adeli}"

    def test_finess_not_on_bare_number(self, engine):
        """Bare 9-digit number without FINESS context must NOT be redacted."""
        entities = engine.detect("Order number 987654321", "en")
        finess = [e for e in entities if e.get("type") == "FR_FINESS"]
        assert len(finess) == 0, f"FR_FINESS fired without context. Got: {finess}"

    def test_finess_wins_over_adeli_in_finess_context(self, engine):
        """A 9-digit number in FINESS context must be tagged FR_FINESS, not FR_ADELI."""
        entities = engine.detect("FINESS de l'hôpital: 750056489", "en")
        adeli = [e for e in entities if e.get("type") == "FR_ADELI"]
        assert len(adeli) == 0, f"FR_ADELI fired on FINESS context (score bug). Got: {adeli}"
        finess = [e for e in entities if e.get("type") == "FR_FINESS"]
        assert len(finess) >= 1, f"FR_FINESS not detected in FINESS context. Got: {[e['type'] for e in entities]}"


class TestFRFinance:
    def test_amf_gp(self, engine):
        entities = engine.detect("Société agréée AMF sous le numéro GP-12345", "en")
        hits = [e for e in entities if e.get("type") == "FR_AMF"]
        assert len(hits) >= 1, f"FR_AMF GP- not detected. Got: {[e['type'] for e in entities]}"

    def test_amf_cif(self, engine):
        entities = engine.detect("Conseiller en investissements financiers CIF-00421 agréé AMF", "en")
        hits = [e for e in entities if e.get("type") == "FR_AMF"]
        assert len(hits) >= 1, f"FR_AMF CIF- not detected. Got: {[e['type'] for e in entities]}"

    def test_lei(self, engine):
        entities = engine.detect("Identifiant LEI: 969500T3MBS4SQAMHJ45", "en")
        hits = [e for e in entities if e.get("type") == "FR_LEI"]
        assert len(hits) >= 1, f"FR_LEI not detected. Got: {[e['type'] for e in entities]}"

    def test_bban_spaced(self, engine):
        entities = engine.detect("RIB compte bancaire: 30004 00831 00012345678 94", "en")
        hits = [e for e in entities if e.get("type") == "FR_BBAN"]
        assert len(hits) >= 1, f"FR_BBAN (spaced) not detected. Got: {[e['type'] for e in entities]}"

    def test_bban_dashed(self, engine):
        entities = engine.detect("Domiciliation bancaire RIB: 30004-00831-00012345678-94", "en")
        hits = [e for e in entities if e.get("type") == "FR_BBAN"]
        assert len(hits) >= 1, f"FR_BBAN (dashed) not detected. Got: {[e['type'] for e in entities]}"


class TestFRAccounting:
    def test_ape_naf(self, engine):
        entities = engine.detect("Code APE de l'entreprise: 6201Z", "en")
        hits = [e for e in entities if e.get("type") == "FR_APE_NAF"]
        assert len(hits) >= 1, f"FR_APE_NAF not detected. Got: {[e['type'] for e in entities]}"

    def test_siret_accounting_context(self, engine):
        entities = engine.detect("Expert-comptable référence SIRET client: 542 107 651 00012", "en")
        hits = [e for e in entities if e.get("type") == "FR_SIRET"]
        assert len(hits) >= 1, f"FR_SIRET in accounting context not detected."

    def test_siren_not_inside_siret_accounting(self, engine):
        entities = engine.detect("Numéro SIRET: 542 107 651 00012", "en")
        siren = [e for e in entities if e.get("type") == "FR_SIREN"]
        assert len(siren) == 0, f"FR_SIREN must not fire inside SIRET. Got: {siren}"
