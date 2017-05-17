# Grammar Processing
--

* grammextract.py: transforms label bracket to Context-free grammar (CFG)

    <b>USAGE:</b> $ python3 gramextract.py -i <inputfile> -o <outputfile> -d <outputdict?> -u <unique sorting?>
    - Input example: [S [NP [NOUN He] ] [VP [VERB owned] [NP [NOUN cars.] ] ] ]
    - Output example (Grammar +unique):

        % S-->NP,VP.

        % NP-->NOUN.

        % VP-->VERB,NP.
    - Output example (Dictionary +dict,+unique)

        % NOUN/cars

        % NOUN/He

        % VERB/owned


* grammarpcfg.py: calculates probability of all CFG

     <b>USAGE:</b> $ python3 grampcfg.py -i <inputfile> -o <outputfile>
     - Input example: a list of CFG
     - Output example (sorted by probability):

        % S-->NP,VP. | Prob:0.29464

        % S-->NP,VP,PP. | Prob:0.08036

        % ...
