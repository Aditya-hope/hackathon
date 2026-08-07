"""
Audit Logger.
"""

from app.core import logger

from app.audit.audit_record import AuditRecord


class AuditLogger:

    def log(
        self,
        record: AuditRecord,
    ) -> None:

        logger.info("=" * 60)

        logger.info("AUDIT RECORD")

        logger.info("=" * 60)

        logger.info(f"Execution ID : {record.execution_id}")

        logger.info(f"Invoice      : {record.invoice_number}")

        logger.info(f"Vendor       : {record.vendor_name}")

        logger.info(f"Risk Score   : {record.risk_score}")

        logger.info(f"Decision     : {record.recommendation}")

        logger.info(f"Provider     : {record.provider}")

        logger.info(f"Time         : {record.processing_time}")

        logger.info("-" * 60)

        for event in record.timeline:

            logger.info(event)

        logger.info("=" * 60)