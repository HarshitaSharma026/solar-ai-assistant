def estimate_power_and_roi(
    square_feet: float,
    efficiency: float = 0.18,
    panel_watt: int = 400,
    cost_per_kw: int = 50000,  # 2025 estimate
    annual_generation_per_kw: int = 1500,  # kWh/year, average
    tariff: float = 9.0  # ₹ per kWh
):
    # area calculations
    usable_area = 0.8 * square_feet  # 80% usable
    area_per_panel = 18  # sq ft per 400w panel
    num_panels = int(usable_area // area_per_panel)
    total_kw = (num_panels * panel_watt) / 1000  # watts to kW

    # cost
    total_cost = total_kw * cost_per_kw

    # savings
    annual_generation = total_kw * annual_generation_per_kw  # kWh/year
    savings_per_year = annual_generation * tariff  # Rs. per year

    # ROI
    roi_years = total_cost / savings_per_year if savings_per_year > 0 else None

    return {
        "total_kw": round(total_kw, 2),
        "estimated_cost_inr": round(total_cost, 2),
        "annual_generation_kwh": int(annual_generation),
        "annual_savings_inr": int(savings_per_year),
        "roi_years": round(roi_years, 1) if roi_years else "N/A",
        "num_panels": num_panels
    }
