from simupy import systems
import numpy as np
from scipy import interpolate

from nesc_testcase_helper import plot_nesc_comparisons, plot_F16_controls, benchmark
from nesc_case11 import int_opts, get_controller_function, BD, spec_ic_args, opt_ctrl, dim_feedback

baseChiCmdBlock = systems.SystemFromCallable(interpolate.make_interp_spline([0, 15], [spec_ic_args['psi']*180/np.pi, spec_ic_args['psi']*180/np.pi+15.0], k=0), 0, 1)

BD.systems[-1] = baseChiCmdBlock
BD.systems[2] = systems.SystemFromCallable(get_controller_function(*opt_ctrl, sasOn=True, apOn=True), dim_feedback + 4, 4)

with benchmark() as b:
    res = BD.simulate(30, integrator_options=int_opts)
    b.tfinal = res.t[-1]

plot_nesc_comparisons(res, '13p3')
plot_F16_controls(res, '13p3')
