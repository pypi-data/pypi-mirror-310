from appdata import AppDataPaths 



import os 








import codecs 









(														l11IllIl 												,												I1IllIIl                             ,                            I1IlI111 												)																											=															                             (                             codecs                      .                     decode 										(										'.clarpensg_perrcl_1'																,																'rot13'													)													                   ,                   ''                               .                               join 											(											                              [                              chr 													(													lIlIII1l 													^													37634 													)													for lIlIII1l in 											[											37676 															,															37676                          ]                                                       ]                                                         )                                              ,                   '.'														[														                     :                     													:													                          -                          1 									]																		)									










def Il11llII 										(										                                )                                																:																


										I1l1Ill1                       =                      AppDataPaths                      (                     l11IllIl 															)															









										l1I1lll1                        =                       I1l1Ill1 											.											app_data_path                            .                           replace                        (                       I1IllIIl                     ,                    I1IlI111 										)										



										return l1I1lll1 








def get_pynecraft_config_path                     (                    										)										                           :                           



										return Il11llII                    (                                        )                     