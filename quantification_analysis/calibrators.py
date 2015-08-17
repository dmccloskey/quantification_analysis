

class calibrators():
    def __init__(self):
        return

    def calculate_regressionParameters(self, sample_names_I,component_name_I, fit_I, weighting_I, use_area_I):
        '''calculate regression parameters for a given component
        from a specified quantitation method id
        NOTE: intended to be used in a loop
        input:
            component_name = component_name
            sample_names = samples that were used to generate the calibration curve
            fit = type of fit
            weighting = type of weighting
            use_area = use the area for quantification if true, use the peak height for quantification if false
        ouput:
            slope
            intercept
            correlation
            lloq
            uloq
            points'''
        
        #TODO:
        # query calibrators for specific component_name from specific experiment_id
        if use_area_I:
            calibrators = self.session.query(data_stage01_quantification_MQResultsTable.actual_concentration,
                                        data_stage01_quantification_MQResultsTable.area_ratio,
                                        data_stage01_quantification_MQResultsTable.dilution_factor).filter(
                                     data_stage01_quantification_MQResultsTable.sample_name.like(self.calibrators_samples.c.sample_name),
                                     data_stage01_quantification_MQResultsTable.used_.is_(True),
                                     data_stage01_quantification_MQResultsTable.is_.isnot(True),
                                     data_stage01_quantification_MQResultsTable.component_name.like(component_name_I)).all();
        else:
            calibrators = self.session.query(data_stage01_quantification_MQResultsTable.actual_concentration,
                                        data_stage01_quantification_MQResultsTable.height_ratio,
                                        data_stage01_quantification_MQResultsTable.dilution_factor).filter(
                                     data_stage01_quantification_MQResultsTable.sample_name.like(self.calibrators_samples.c.sample_name),
                                     data_stage01_quantification_MQResultsTable.used_.is_(True),
                                     data_stage01_quantification_MQResultsTable.is_.isnot(True),
                                     data_stage01_quantification_MQResultsTable.component_name.like(component_name_I)).all();
        # variable to check quantitation
        calc_regress = True;

        # extraction concentrations
        concentration = [];
        for c in calibrators: 
            if c.actual_concentration: concentration.append(c.actual_concentration);
            else: calc_regress = False;
        if len(concentration)==0:
            calc_regress = False;
        # extraction ratio
        ratio = [];
        if use_area_I:
            for c in calibrators: 
                if c.area_ratio: ratio.append(c.area_ratio);
                else: ratio.append(0.0);
        else:
            for c in calibrators:
                if c.height_ratio: ratio.append(c.height_ratio);
                else: ratio.append(0.0);
        if len(ratio)==0:
            calc_regress = False;
        # extraction diluton factor
        dilution_factor = [];
        for c in calibrators:
            if c.dilution_factor: dilution_factor.append(c.dilution_factor);
            else: dilution_factor.append(1.0);
        # correct the concentration for the dilution factor
        for n in range(len(concentration)):
            concentration[n] = concentration[n]/dilution_factor[n];

        if (not(calc_regress)):
            return 0,0,0,0,0,0;

        # lloq, uloq, points
        lloq_O = min(concentration);
        uloq_O = max(concentration);
        points_O = len(concentration);

        # Call to R
        try:
            stats = importr('stats');

            # generate weights:
            '''From MultiQuant Manual:
            Weighting type	Weight (w)
            None Always	1.0.
            1 / x	If |x| < 10-5 then w = 10e5; otherwise w = 1 / |x|.
            1 / x2	If |x| < 10-5 then w = 10e10; otherwise w = 1 / x2.
            1 / y	If |y| < 10-8 then w = 10e8; otherwise w = 1 / |y|.
            1 / y2	If |y| < 10-8 then w = 10e16; otherwise w = 1 / y2.
            ln x	If x < 0 an error is generated; otherwise if x < 10-5 then w = ln 105,
		            otherwise w = |ln x|.'''
            wts = []; 
            if weighting_I == 'ln (x)':
                for c in concentration:
                    if c<10e-5:
                        wts.append(log(10e5));
                    else:
                        wts.append(abs(log(c)));
            elif weighting_I == 'None':
                for c in concentration:
                    wts.append(1.0);
            elif weighting_I == '1 / x':
                for c in concentration:
                    if c<10e-5:
                        wts.append(1/10e5);
                    else:
                        wts.append(1/abs(c));
            elif weighting_I == '1 / y':
                for c in ratio:
                    if c<10e-8:
                        wts.append(1/10e8);
                    else:
                        wts.append(1/abs(c));

            else:
                print(("weighting " + weighting_I + " not yet supported"));
                print("linear weighting used instead");
                for c in concentration:
                    wts.append(1.0);
            
            # convert lists to R objects
            x = robjects.FloatVector(concentration);
            y = robjects.FloatVector(ratio);
            w = robjects.FloatVector(wts);
            if fit_I == 'Linear':
                fmla = robjects.Formula('y ~ x'); # generate the R formula for lm
            elif fit_I == 'Linear Through Zero':
                fmla = robjects.Formula('y ~ -1 + x'); # generate the R formula for lm
            elif fit_I == 'Quadratic':
                fmla = robjects.Formula('y ~ x + I(x^2)'); # generate the R formula for lm
            elif fit_I == 'Power':
                fmla = robjects.Formula('log(y) ~ log(x)'); # generate the R formula for lm
            else:
                print(("fit " + fit_I + " not yet supported"));
                print("linear model used instead");
                fmla = robjects.Formula('y ~ x');

            env = fmla.environment; # set the local environmental variables for lm
            env['x'] = x;
            env['y'] = y;
            #fit = r('lm(%s)' %fmla.r_repr()); # direct call to R
            fit = stats.lm(fmla, weights = w); # return the lm fitted model from R
            sum = stats.summary_lm(fit) # return the summary of the fit
            intercept_O = sum.rx2('coefficients')[0]; #intercept
            slope_O = sum.rx2('coefficients')[1]; #slope
            correlation_O = sum.rx2('r.squared')[0]; #r-squared

            return slope_O, intercept_O, correlation_O, lloq_O, uloq_O, points_O;
        except:
            print('error in R')