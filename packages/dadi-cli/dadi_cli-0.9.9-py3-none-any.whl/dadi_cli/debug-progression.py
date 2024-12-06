import dadi
import dadi.DFE
import pickle
from dadi.LowPass.LowPass import make_low_pass_func_GATK_multisample as func_cov

cov_dist_syn = pickle.load(open("examples/results/lowpass/mus.syn.fs.coverage.pickle",'rb'))
cov_dist_nsyn = pickle.load(open("examples/results/lowpass/mus.nonsyn.fs.coverage.pickle",'rb'))



dadi.Demographics2D.split_mig([1,1,0.1,1], fs.sample_sizes, 10)
dadi.Numerics.make_anc_state_misid_func(dadi.Demographics2D.split_mig)([1,1,0.1,1,0.1], fs.sample_sizes, 10)
dadi.Numerics.make_extrap_func(dadi.Numerics.make_anc_state_misid_func(dadi.Demographics2D.split_mig))([1,1,0.1,1,0.1], fs.sample_sizes, [10,20,30])

func_cov(dadi.Demographics2D.split_mig, cov_dist_syn, fs.pop_ids, [10, 16], [4, 8])([1,1,0.1,1], [4, 8], 10)
func_cov(dadi.Numerics.make_extrap_func(dadi.Numerics.make_anc_state_misid_func(dadi.Demographics2D.split_mig)), cov_dist_syn, fs.pop_ids, [10, 16], fs.sample_sizes)([1,1,0.1,1,0.1], fs.sample_sizes, [10,20,30])



cache1d.integrate([1,1], fs.sample_sizes, dadi.DFE.PDFs.lognormal, 2000)
dadi.Numerics.make_anc_state_misid_func(cache1d.integrate)([1,1,0.1], [4, 8], dadi.DFE.PDFs.lognormal, 2000)

# make_low_pass_func_GATK_multisample(func, cov_dist, pop_ids, nseq, nsub)
# nseq is max samples
# nsub is the projected samples
func_cov(cache1d.integrate, cov_dist_nsyn, fs.pop_ids, [10, 16], [4, 8])([1,1], [4, 8], dadi.DFE.PDFs.lognormal, 2000)