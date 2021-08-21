/*
	Authors: Nausheen Saba Shahid and Kostas Stathis
	Date: Jan 2020
	Created: Nov 2019
*/


/*  L=
[
		set(cooperationcost(1)),
		set(cooperationbenefit(10)),
		set(starttime(0)),
		set(rounds(1,2)),
%    	        make(1,conductor(1,2,3)),
%		make(1,player(alwayscooperate,no,no)),
%		make(1,player(alwaysdefect,no,no)),
%	        make(1,player(titfortat,1,no)),
                generationinfo(Nc,N),
                output(resultsin('resultsexp1.pl')),
		output(eventsin('historyexp1.pl'))
         ]

*/




set(L):-
   assert(L). 

output(L):-
 assert(L). 



run(L):-
      forall(member(Config, L),call(Config)),
      generationinfo(Nc,N),
      starttime(Ts),                       %write('----------'),
      evolve_all_for(gens(Nc,N),[Ts,Te]).


evolve_all_for(gens(N,N),[Te,Te]):-  
 	!, 	
        halt_at(Te).




evolve_all_for(gens(Nc,N), [Ts,Te]):-       %   Ni \= N,              
%	initialize_at(gen(Nc,Ti,Tj),Ts),    write(' Initializing the generation at '), write(Ti),
        Ti is Ts + 1,
        Tj is Ti + 30,
       	evolve_one_for(gen(Nc),[Ti, Tj]),  write('fully evolution Time: '),write(Ti),writeln(Tj),
        NewN is Nc + 1, 
	!,
        evolve_all_for(gens(NewN,N), [Tj,Te]) .       
  
 
% final round
evolve_one_for(gen(Nc),[Ti,Tj]):-  write(' LAst case time interval :'), write(Ti),write(Tj),
   Ti>Tj,
   !. 


 
% typical round
evolve_one_for(gen(Nc), [Ts, Tk]):-   write('normal ending time of generation: '),write(Te),                                      %  Ti<= Te, 
     print_cycle(Ts),                                        %   env_step(Ti),
%     consume_at(gen(Nc), Es,Ts),                                     % collect attempts
     display_at(gen(Nc), [cooperate(agent1,agent2)], Ts),                                 % execute --- happens_at
      Tj is Ts+1,  
     !, 
     evolve_one_for(gen(Nc),[Tj, Tk]).

 

        
    
% displaying attempts and notifying them at time T
display_at(gen(Nc), Es, T):-                                                                  %  writeln('\n...............Following events have happened in this cycle.................... '),length(Es,L), writeln(L),
	forall(member(E, Es), (update_at(E, T), process_event(E, T))).                        /* implicit notification takes place here  */

% process_event(E).


print_cycle(T):-
	write('\n______________________________________Cycle number: '),
        write(T),
        writeln('______________________________________').
          
      
update_at(E, T):-
	write('\n______________________________________Event Happened: '),
        writeln("").
        









        
halt_at(T).


final(T):-
        %holds_at(simulation=end,T),
        T>9,  
        simulation_explanation(T).




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5555


run_simulation(Nc,N,Ts,Te):-                    % total number of generations, starting time
	evolve_all_for(gens(Nc,N), [Ts,Te]).              % current generation, total number of generations, starting time
  
 
run_simulation_from_mid(Nc,N,Ti,Te):-
	update_at(set(currentGeneration=Nc),Ti),  % write(' generation'),
     	evolve_all_for(gens(Nc,N), [Ti,Te]).                     % current generation, total number of generations, starting time

 



run_experiment(Start,End):-
   Start>End,
   !. 


run_experiment(Start,End):-
    atom_concat('trail', Start, S),
    assert(trailnumber(S)),
    config_of(general,numberOfGeneration,Gen),                          
    run_simulation(0,Gen,0,Te),                    % total number of generations, starting time
    NewStart is Start+1, 
    retract(trailnumber(S)),!, %write('New Experiemnt'),
    run_experiment(NewStart,End).                    
