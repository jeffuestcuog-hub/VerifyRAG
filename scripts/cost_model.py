"""Transparent cost scenario; estimates are never labelled measured savings."""
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]

def calculate(input_tokens, output_tokens, input_rate, output_rate, queries,
              saved_minutes, hourly_value, build_hours, accepted_fraction):
    api_per_query = (input_tokens*input_rate + output_tokens*output_rate)/1_000_000
    api_monthly = api_per_query * queries
    gross_value = queries * accepted_fraction * saved_minutes / 60 * hourly_value
    net_monthly = gross_value - api_monthly
    build_cost = build_hours * hourly_value
    return {'label': 'ILLUSTRATIVE SCENARIO, NOT MEASURED ROI',
            'api_cost_usd_per_query': api_per_query, 'api_cost_usd_per_month': api_monthly,
            'gross_time_value_usd_per_month': gross_value, 'net_time_value_usd_per_month': net_monthly,
            'one_time_build_opportunity_cost_usd': build_cost,
            'payback_months': build_cost/net_monthly if net_monthly>0 else None,
            'excluded': ['Hosting', 'Maintenance', 'Evidence review overhead beyond entered net saved minutes',
                         'Provider-routing premiums', 'Failed/retried requests', 'Taxes and credit-purchase fees'],
            'interpretation': 'Time value is capacity released, not automatically cash savings.'}

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input-tokens', type=int, default=3500)
    p.add_argument('--output-tokens', type=int, default=350)
    p.add_argument('--input-rate', type=float, required=True, help='Verified USD per million input tokens')
    p.add_argument('--output-rate', type=float, required=True, help='Verified USD per million output tokens')
    p.add_argument('--queries', type=int, default=1600)
    p.add_argument('--saved-minutes', type=float, default=2)
    p.add_argument('--hourly-value', type=float, default=40)
    p.add_argument('--build-hours', type=float, default=30)
    p.add_argument('--accepted-fraction', type=float, default=.7)
    a = p.parse_args()
    values = vars(a)
    if any(v<0 for v in values.values()) or not 0<=a.accepted_fraction<=1:
        p.error('Inputs must be non-negative; accepted fraction must be between 0 and 1.')
    print(json.dumps({'assumptions': values, 'results': calculate(**values)}, indent=2))
