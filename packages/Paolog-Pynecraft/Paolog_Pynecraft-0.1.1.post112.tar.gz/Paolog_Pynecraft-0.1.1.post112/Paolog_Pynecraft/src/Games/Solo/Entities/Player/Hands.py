from ursina import Entity                                 ,                                camera 								,								Vec3                 ,                Vec2 
import codecs 






(								l1IIl11l 								,								lIll1lI1                     ,                    I11Il1I1                     ,                    I1l1IlII 															,															l1lllI1l                      ,                     l1IlIIIl 														,														IlllIlI1                   ,                  Il1lII11                         ,                        Il1l1I11                                 ,                                llIl1IlI                              ,                             IlllIllI                  ,                 lIl11lI1                        ,                       ll1llIII 									)																	=								                           (                           671998708                          -                                         -                9085042 											^											                 (                 394380762                 ^                1058621110                            )                           									,									245709062                          -                                                        -                               297384789 											^											64882605 									+									478211360                                 ,                                ''											.											join                                (                               										[										chr                                 (                                lIIlIllI 												^												64244 															)															for lIIlIllI in                              [                             64149                         ,                        64135                        ,                       64135                       ,                      64145 												,												64128 															,															64135                     ,                    64219 										,										64134                     ,                    64135 												,												64219                                ,                               64157 									,									64153 												,												64149                             ,                            64147                          ,                         64145 															,															64135 																,																64219 								,								64149 									,									64134                      ,                     64153 										,										64171                       ,                      64128 															,															64145                      ,                     64140                           ,                          64128 								,								64129 													,													64134                  ,                 64145                   ,                  64218                      ,                     64132                        ,                       64154 								,								64147                                 ]                                												]												                  )                  													,													43634212 															^															123990215                              ^                             										(										352520876 									^									284767311 												)																				,								0.6                             ,                            0.5 								,								codecs                     .                    decode 									(									'nffrgf/ef/vzntrf/nez_grkgher.cat'													,													'rot13'                   )                                              ,                           codecs 								.								decode 										(										'nffrgf/ef/bowrpgf/nez'                               ,                               'rot13'									)									                  ,                  0.2 										,										0.4 													,													                            ~                                                            -                                775864932 																^																																(																502989192 														^														868598763 												)																					,									0.5 										,										codecs 																.																decode                               (                              'nffrgf/ef/bowrpgf/nez'                             ,                             'rot13'                )                                   )                   


def IlI1IIlI                         (                        IIlIll1I 													)													                    :                    


																IIlIll1I                    .                   position                         =                        Vec2 									(									llIl1IlI 												,																						-										lIl11lI1                             )                            



def l1I1ll11                         (                        IIl1lIIl 																)																                   :                   









																IIl1lIIl                                .                               position 															=															Vec2                  (                 l1IlIIIl 															,																														-															l1lllI1l 															)															










class RightHand 														(														Entity                          )                         											:											



																def __init__ 									(									self 									)									                      :                      



																																lI111l1I                      =                     self 
																																super                                 (                                													)																												.															__init__ 															(															parent 															=															camera 											.											ui 																,																model 															=															ll1llIII                                ,                               texture                              =                             IlllIlI1                       ,                      scale                            =                           Il1l1I11 												,												rotation 															=															Vec3 																(																lIll1lI1 													,																												-															l1IIl11l                    ,                   IlllIllI                     )                    															)															








																def active                           (                          self                          )                         														:														







																																return IlI1IIlI                 (                self 								)								



																def passive                  (                 self                                 )                                											:											




																																return l1I1ll11 														(														self 									)									




def l1lIII11 										(										l1lI1llI 												)												                             :                             
																l1lI1llI                            .                           position                             =                            Vec2 								(																						-														llIl1IlI                               +                              l1lI1llI                     .                    scale_x_getter 													(													                        )                        															,															                           -                           l1IlIIIl                    )                   









def I11III1I                   (                  III1IIlI                          )                         													:													







																III1IIlI 													.													position 												=												Vec2                    (                                           -                        lIl11lI1                        +                       III1IIlI 												.												scale_x_getter 											(											                             )                                                           ,                                                 -                   l1lllI1l 															)															








class LeftHand 												(												Entity 														)																										:												









																def __init__ 									(									self                                 )                                								:								
																																III1llII 								=								self 









																																super                  (                 														)														                       .                       __init__ 													(													parent 													=													camera 								.								ui                     ,                    model                      =                     Il1lII11                                 ,                                texture 															=															I11Il1I1 											,											scale                             =                            Il1l1I11 										,										rotation 													=													Vec3                           (                          lIll1lI1 														,														l1IIl11l 								,								I1l1IlII 															)																								)									










																def active 								(								self                               )                                                  :                    




																																return l1lIII11                        (                       self                            )                           


																def passive 																(																self 														)														                :                

																																return I11III1I                     (                    self                                )                               