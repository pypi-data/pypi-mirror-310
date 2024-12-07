import warnings

import pandas as pd
from scipy.optimize import minimize

from IRS_toolkit.core.leg import fix_leg, float_leg
from datetime import datetime
from dateutil.relativedelta import relativedelta
from IRS_toolkit.core.curve import compounded, yield_curve
from IRS_toolkit.utils.constants import VALID_FILL_TYPE,VALID_CONVENTIONS
from IRS_toolkit.utils import schedule

warnings.filterwarnings("ignore")


class Swap:
    """
    A class that provides various outputs related to swap pricing.


    Args:
        fix_leg (legFix): fixed leg
        float_leg (legFloat): float leg
    """

    def __init__(self,
                nominal:float,
                fix_rate:float=None,
                yield_curve:yield_curve.YieldCurve=None,
                ESTR_compounded:compounded.Compounded=None,
                schedule_fix:schedule.Schedule=None,
                schedule_float:schedule.Schedule=None,
                relative_delta=None):

        self.nominal=nominal
        self.fix_rate=fix_rate
        self.yield_curve=yield_curve
        self.ESTR_compounded=ESTR_compounded
        self.schedule_fix=schedule_fix
        self.schedule_float=schedule_float
        self.relative_delta=relative_delta

        fix_leg_object=fix_leg.FixLeg(nominal=nominal,
        fix_rate=fix_rate,
        schedule=schedule_fix)

        float_leg_object=float_leg.FloatLeg(nominal=nominal,
                                            yield_curve_object=yield_curve,
                                            schedule=schedule_float,
                                            ESTR_coumpounded=ESTR_compounded,
                                            relative_delta=relative_delta)

        self.fix_leg_object = fix_leg_object
        self.float_leg_object = float_leg_object

    def npv(self, valuation_date:datetime):
        """
        Net present value of the swap

        Args:
            discount_curve (curve): yield curve
            date_valo (date, optional): valuation date. Defaults to None.
            RunningCouv (float, optional): spread. Defaults to 0.00.
            GainGC (float, optional): spread. Defaults to 0.00.

        Returns:
            float: Net present value
        """
        self.fix_leg_object.discount_cashflow(self.yield_curve, valuation_date)
        self.float_leg_object.discount_cashflow(self.yield_curve, valuation_date)
        self.NPV_ = self.fix_leg_object.NPV - self.float_leg_object.NPV
        return self.NPV_

    def fair_rate(self, valuation_date:datetime):
        """
        fair rate of the swap

        Args:
            date_valo (date): date valuation
            ImpSchedule (dataframe) : in case you use imported schedule

        Returns:
            float, float: fair rate, theorical fair rate
        """
        fix_rate = self.fix_leg_object.fix_rate

        fix_leg_object_nominal=self.fix_leg_object.nominal
        fix_leg_object_schedule=self.fix_leg_object.schedule

        def loss_func(fix_rate:float):
            leg_fix = fix_leg.FixLeg(
                nominal=fix_leg_object_nominal,
                fix_rate=fix_rate,
                schedule=fix_leg_object_schedule,
            )
            leg_fix.compute_cash_flow(pd.Timestamp(valuation_date))
            leg_fix.discount_cashflow(self.float_leg_object.yield_curve_object, valuation_date)
            return (leg_fix.NPV - self.float_leg_object.NPV) * (
                leg_fix.NPV - self.float_leg_object.NPV
            )

        res = minimize(
            loss_func,
            fix_rate,
            method="nelder-mead",
            options={"xatol": 1e-8, "disp": True},
        )
        self.faire_rate = float(res.x)
        self.faire_rate_theory = (
            self.float_leg_object.NPV
            / (
                self.fix_leg_object.nominal
                * self.fix_leg_object.cashflow.iloc[:, 3]
                * self.fix_leg_object.cashflow.DF
            ).sum()
        )
        return self.faire_rate, self.faire_rate_theory

    def price(self, valuation_date:datetime,spreadHC:float,spreadGC:float):
        if self.relative_delta is None:
            relative_delta=relativedelta(days=0)
        else:
            relative_delta=self.relative_delta

        self.fix_leg_object.compute_cash_flow(valuation_date, spreadHC, spreadGC)
        self.fix_leg_object.discount_cashflow(self.yield_curve, valuation_date, relative_delta)

        self.float_leg_object.compute_cash_flow(valuation_date)
        self.float_leg_object.discount_cashflow(self.yield_curve, valuation_date, relative_delta)
