import quantsbin.derivativepricing as qbdp
import matplotlib.pyplot as plt
plt.clf()

fx_option = qbdp.FXOption(option_type='Call', expiry_type='EUROPEAN', strike=1.25, expiry_date='20190620')

# plot payoff
eq1_payoff = qbdp.Plotting(equity_option1, 'payoff', x_axis_range=[25, 75]).line_plot()
eq1_payoff.show()

# option pricing and greeks
eq1_engine = fx_option.engine(model='BSM', pricing_date='20180620', spot0=55, rf_rate=0.05, volatility=0.25)
print(eq1_engine.valuation())  # premium
print(eq1_engine.risk_parameters())  # valuation

# plot pnl
eq1_pnl = qbdp.Plotting(eq1_engine, 'pnl', x_axis_range=[25, 75]).line_plot()
eq1_pnl.show()

# plot premium and payoff together for different spots
eq1_payoff = qbdp.Plotting(equity_option1, 'payoff', x_axis_range=[25, 75]).line_plot()
eq1_pnl = qbdp.Plotting(eq1_engine, 'valuation', x_axis_range=[25, 75]).line_plot()


# plot greeks
plt.cla()
qbdp.Plotting(eq1_engine, 'delta', x_axis_range=[25, 75]).line_plot()
plt.cla()
qbdp.Plotting(eq1_engine, 'gamma', x_axis_range=[25, 75]).line_plot()
plt.cla()
qbdp.Plotting(eq1_engine, 'theta', x_axis_range=[25, 75]).line_plot()
plt.cla()
qbdp.Plotting(eq1_engine, 'vega', x_axis_range=[25, 75]).line_plot()
plt.cla()
qbdp.Plotting(eq1_engine, 'rho', x_axis_range=[25, 75]).line_plot()