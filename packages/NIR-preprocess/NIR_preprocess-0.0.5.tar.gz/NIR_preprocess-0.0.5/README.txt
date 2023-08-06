Package NIR_preprocess includes: 
    - function compare_preprocessing

Available at www.pypi.org

PROJECT DESCRIPTION
Function compare_preprocessing can be used on any NIR spectral data if Y values are available. 
Y can include one or several variables.

Function evaluates impact of different pre-processing techniques and combinations using multiblock partial least squares (MBPLS). Each block in MBPLS is a pre-processed spectral data. 

Different pre-processing techniques evaluated:
    - baseline
    - de-trend
    - EMSC
    - MSC
    - SNV
    - Savitzky Golay derivatives (different polynomial and derivatives orders can be tested as well as the size of the moving window)

Blocks in MBPLS include: 
    - pre-processing techniques and combinations (several techniques applied to same data)
    - original spectral data (starting point)
    - 20 blocks of random noise called false signals (reference for destroyed information)
    
Analyst can choose to only compare scatter corrections techniques or only derivatives or both. It is also possible to set the number of pre-processing techniques which can be applied to one same data. By default, only a single pre-processing technique and a combination of 2 are tested. NB: EMSC and MSC can not be applied together
    
For MBPLS, analyst can choose: 
    - number of principal components
    - to autoscale or center each block
    - to autoscale or center Y
    
Blocks are represented in superloading plots.
Model performances (adjusted R2, RMSECV) and variable importance on projection (VIP) are calculated for each block by cross validation. Number of random picks for cross validation and number of lines predicted in each cross validation can be set by the analyst. Effective rank for each block is calculated as well. 


FUNCTION DETAILS
[ combination, datasets, datasets0, R2_all,  R2adj_all, RMSECV_all, VIP_all, W] = compare_preprocessing(X0, y ,nbPC=2, nb_comb=2, auto_x=1, auto_y=1, nb=1, CVnb=20, only_sg=0, svg_order=[1,2], svg_deriv = [1,2], svg_window = [13,15,17], sg_op=0)
    
1. INPUT ARGUMENTS
    X0 [n x k] <numpy.ndarray>
        X0 data to test pre-processing techniques on
        n samples
        k variables
    y [n x m] <numpy.ndarray>
        y data under study
        n samples
        m variables
        
2. OPTIONAL INPUT ARGUMENTS    
    nbPC <int>
        number of principal components for PLS in the MBPLS decomposition (default value=2)
    nb_comb <int>
        maximum number of pre-processing techniques applied on same data (default value=2)      
    auto_x <int>
        autoscale data after applying pre-processing technique if auto_x=1, if not data centered (default value=1)
    auto_y <int>
        autoscale variables to predict if auto_y=1, if not centered (default value=1)
    nb <int>
        number of random picks for cross validation
    CVnb <int>
        number of samples predicted in each cross validation
    only_sg <int>
        only test Savitzky-Golay if only_sg=1 (default value=0)
    svg_order <list>
        Savitzky-Golay polynomials orders to test
    svg_deriv <list>
        Savitzky-Golay derivatives orders to test
    svg_window <list>
        Savitzky-Golay window sizes to test
    sg_op <int>
        test only Savitzky-Golay pretreatments with the same order of polynomial and derivative if sg_op=0 (default value=0)
        
3. OUTPUT
    combination <list>
        Pre-processing options tested
    datasets <list>
        data X0 after each pre-processing option and autoscaled or centered
    datasets0 <list>
        data X0 after each pre-processing option     
    R2_all <list>   
        R2 values for each y variable predicted for each pre-processing option tested (block)
    R2adj_all <list>   
        R2 adjusted values for each y variable predicted for each pre-processing option tested (block)
    RMSECV_all <list>   
        Root mean square error by cross validation for each y variable predicted for each pre-processing option tested (block)
    VIP_all <list>   
        PLS variable importance in projection for each y variable predicted for each pre-processing option tested (block) 
    Wt <numpy.ndarray>
	Superloadings from MBPLS

EXAMPLES
Two full examples, along with datasets are provided in 'Download Files'. Please refer to 'NIR_preprocess_example.pdf' for full details
    - Example 1: Artificial dataset
    - Example 2: Corn dataset

COMPATIBILITY
compare_preprocessing tested on Python 3.8 using the following modules:
    - numpy 1.19.2
    - matplotlib 3.3.2
    - copy
    - itertools
    - RG 0.0.66 (available from Pypi at: https://pypi.org/project/RG/)