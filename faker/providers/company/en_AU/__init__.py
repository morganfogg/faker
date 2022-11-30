from typing import Optional, Tuple

from .. import Provider as CompanyProvider


class Provider(CompanyProvider):
    def abn(self, acn: Optional[int] = None) -> int:
        """
        Generate an Australian Business Number (ABN). Consists of 9 significant digits (usually the
        same as the company's ACN) preceded by two check digits. The check digit algorithm is
        described here: https://abr.business.gov.au/Help/AbnFormat
        """

        if acn is None:
            acn = self.acn()

        acn_digits = [int(digit) for digit in f"{acn:09}"]
        weights = range(3, 21, 2)

        checksum_total = sum(digit * weight for digit, weight in zip(acn_digits, weights))

        next_multiple_of_89 = ((checksum_total // 89) + 1) * 89

        check_digit = next_multiple_of_89 - checksum_total + 10

        return check_digit * 1_000_000_000 + acn

    def acn(self) -> int:
        """
        Generate an Australian Company Number (ACN). Consists of 8 significant digits followed by a
        check digit. The check digit algorithm is described here:
        https://asic.gov.au/for-business/registering-a-company/steps-to-register-a-company/australian-company-numbers/australian-company-number-digit-check/
        """

        acn_base = self.random_int(min=0, max=99_999_999)
        acn_digits = [int(x) for x in f"{acn_base:08}"]
        weights = range(8, 0, -1)

        checksum_total = sum(digit * weight for digit, weight in zip(acn_digits, weights))
        check_digit = 10 - (checksum_total % 10)

        if check_digit == 10:
            check_digit = 0

        return acn_base * 10 + check_digit

    def abn_acn(self) -> Tuple[int, int]:
        """
        Generates a matching ABN and ACN. The last 9 digits of a company's ABN are usually the same
        as their ACN.
        """
        acn = self.acn()
        abn = self.abn(acn)

        return abn, acn
