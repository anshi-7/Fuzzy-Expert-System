# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 11:27:20 2020

@author: Anshi Srivastav
"""

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

#Now Antecedent/Consequent objects hold universe variables and membership functions
m = ctrl.Antecedent(np.arange(0, 0.75, 0.05), 'Mean Delay')
s = ctrl.Antecedent(np.arange(0, 1.05, 0.05), 'Number of Servers')
p = ctrl.Antecedent(np.arange(0, 1.05, 0.05), 'Repair Utilization Factor')
n = ctrl.Consequent(np.arange(0, 1.05, 0.05), 'Number of Spares')   #this is output.

#Generate fuzzy membership functions
m['Very Small'] = fuzz.trapmf(m.universe, [0, 0, 0.1, 0.3])   #numerical ranges
m['Small'] = fuzz.trimf(m.universe, [0.1, 0.3, 0.5])
m['Medium'] = fuzz.trapmf(m.universe, [0.4, 0.6, 0.7, 0.7])
s['Small'] = fuzz.trapmf(s.universe, [0, 0, 0.15, 0.35])
s['Medium'] = fuzz.trimf(s.universe, [0.3, 0.5, 0.7])
s['Large'] = fuzz.trapmf(s.universe, [0.6, 0.8, 1, 1])
p['Low'] = fuzz.trapmf(p.universe, [0, 0, 0.4, 0.6])
p['Medium'] = fuzz.trimf(p.universe, [0.4, 0.6, 0.8])
p['High'] = fuzz.trapmf(p.universe, [0.6, 0.8, 1, 1])
n['Very Small'] = fuzz.trapmf(n.universe, [0, 0, 0.1, 0.3])
n['Small'] = fuzz.trimf(n.universe, [0, 0.2, 0.4])
n['Rarely Small'] = fuzz.trimf(n.universe, [0.25, 0.35, 0.45])
n['Medium'] = fuzz.trimf(n.universe, [0.3, 0.5, 0.7])
n['Rarely Large'] = fuzz.trimf(n.universe, [0.55, 0.65, 0.75])
n['Large'] = fuzz.trimf(n.universe, [0.6, 0.8, 1])
n['Very Large'] = fuzz.trapmf(n.universe, [0.7, 0.9, 1, 1])
m.view()
s.view()
p.view()
n.view()

#Rules
rule1 = ctrl.Rule(p['Low'], n['Small'])    # in the form of if-then
rule2 = ctrl.Rule(p['Medium'], n['Medium'])
rule3 = ctrl.Rule(p['High'], n['Large'])
rule4 = ctrl.Rule(m['Very Small'] & s['Small'], n['Very Large'])
rule5 = ctrl.Rule(m['Small'] & s['Small'], n['Large'])
rule6 = ctrl.Rule(m['Medium'] & s['Small'], n['Medium'])
rule7 = ctrl.Rule(m['Very Small'] & s['Medium'], n['Rarely Large'])
rule8 = ctrl.Rule(m['Small'] & s['Medium'], n['Rarely Small'])
rule9 = ctrl.Rule(m['Medium'] & s['Medium'], n['Small'])
rule10 = ctrl.Rule(m['Very Small'] & s['Large'], n['Medium'])
rule11 = ctrl.Rule(m['Small'] & s['Large'], n['Small'])
rule12 = ctrl.Rule(m['Medium'] & s['Large'], n['Very Small'])
rule1.view()
rule2.view()
rule3.view()
rule4.view()
rule5.view()

#Rule Application
#What would be the number of spares in the following circumstances:
##
#Mean Delay was 0.5
#Number of Servers was 0.3
#Repair Utilization Factor was 0.2
#We need the activation of our fuzzy membership function at these values.
ServiceCentre_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12])
ServiceCentre = ctrl.ControlSystemSimulation(ServiceCentre_ctrl)
#Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
ServiceCentre.input['Mean Delay'] = 0.5
ServiceCentre.input['Number of Servers'] = 0.3
ServiceCentre.input['Repair Utilization Factor'] = 0.2

#Crunch the numbers
ServiceCentre.compute()
t=(ServiceCentre.output['Number of Spares'])
print("This is available number of spares:",t)
n.view(sim=ServiceCentre)
