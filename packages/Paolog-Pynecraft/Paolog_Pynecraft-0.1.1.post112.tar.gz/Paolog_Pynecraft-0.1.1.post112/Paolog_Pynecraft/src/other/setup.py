import os 







from 												.												get_config_path import get_pynecraft_config_path as conf_path 
from 															.															settings import create_node 







import codecs 









(                         llIl1l11 													,													llIll1lI 													)													                        =                        									(									''															.															join                                (                                                 [                  chr                  (                 llI1Ill1 															^															53375 											)											for llI1Ill1 in 											[											53295                            ,                           53286                 ,                53297 											,											53306                                 ,                                53308 											,											53293 										,										53310 									,									53305                  ,                 53291                          ]                         												]																												)																										,										codecs 											.											decode                      (                     b'2f776f726c6473'								,								'hex'                          )                                                      .                            decode 												(												'utf-8'															)															                               )                               





def l11I111l 								(								                             )                                                     :                        

														os 									.									mkdir 								(								conf_path 									(																		)																					)												







														create_node 										(										llIl1l11                          )                         









														os 								.								mkdir 											(											conf_path                   (                  											)											                      +                      llIll1lI 											)											




def setup_pynecraft                  (                 								)								                              :                              
														return l11I111l                       (                                      )                