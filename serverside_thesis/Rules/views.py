import datetime,json,urllib2, urllib

from django.shortcuts import render
# checks if an objects exists of not
from django.shortcuts import get_object_or_404 
from Disease.models import Disease
from Evidence.models import Evidence
from rest_framework import generics
from rest_framework.fields import empty
from rest_framework.views import APIView  # returns API Data
from rest_framework.response import Response # returns response
from Rules.models import Rule
from Rules.serializers import QuestionSerializer
   

class Examine(APIView):


    def get(self,request,parameters,target):
        """
            This function will display the next question based on the user's 
                answered question or it will display the result when no more 
                question can be asked.

            Args: parameters (string) - This is either a "start" string which 
                means that no question are answered; or this could be the 
                evidence id of the question answered followed by an arrow ('=')
                and followed by the certainty factor of the evidence; the answer
                of the user is represented by 1 and -1 which representes yes and 
                no in that order. The answers are seperated by comma. 
                    Eg. 1=1,2=-1

            target (string) - the target disease that this function must
                investigate.

            Returns: data (json) - A json response of the question or the list 
                                    of result base on the disease.
        """

        def combine_multiple_rules_with_the_same_conclusion(to_change_cf,raw_cf):
            """
                This funcion combines to certainty factor into one.

                Args: to_change_cf (float) - Represents the base certainty 
                                                factor.

                      raw_cf - Represents the cf that will be combined 

                Returns: combined_cf (float) - The combined certainty 
                                factor of the two parameters

            """
            combined_cf = 0

            if to_change_cf != 0:
                #Formula for combining the Certainty Factor of the two
                if to_change_cf >= 0 and raw_cf >= 0:
                    # Both Positive
                    combined_cf = to_change_cf + raw_cf - (to_change_cf * raw_cf)
                elif to_change_cf < 0 and raw_cf < 0:
                    # Both Negative
                    combined_cf = to_change_cf + raw_cf + (to_change_cf * raw_cf)
                else:
                    # Different Signs
                    combined_cf = (to_change_cf + raw_cf) / (1.0 - \
                        (min(abs(to_change_cf),abs(raw_cf))))    
            else:
                combined_cf = float(raw_cf)
            return combined_cf


        def conjuct_certainty_factors(to_conjuct_first,to_conjuct_second):
            """
                This function is when two values are to conjucted (and condition). 

                Args: to_conjuct_first (float) - The first value to be combine
                       to_conjuct_second (float) - The second value to be combine

                Returns (float): The minimum of the two values
            """
            return min(to_conjuct_first,to_conjuct_second)


        def disjunct_certainty_factor(to_conjuct_first,to_conjuct_second):
            """
                This function is when two values are to disjuct (or condition). 

                Args: to_conjuct_first (float) - The first value to be combine
                       to_conjuct_second (float) - The second value to be combine

                Returns (float): The maximum of the two values
            """
            return max(to_conjuct_first,to_conjuct_second)



        def remove_innermost_parenthesis(current_condition,highest_priority):
            """
                This function removes matching parenthesis that has no available
                    combination of cf

                Args: current_condition (string) - The current condition in 
                        string form
                      
                      highest_priority (int) - The priority that the function
                            has to remove. This just means the innermost 
                            parenthesis since the highest priority of an 
                            equation is the innermost one.

                Returns: cleaned_condition (string) - returns a new current 
                            condition without the "highest" parenthesis 
                            for further evaluation.
            """
            priority = 0
            cleaned_condition = ""
            for element in current_condition:
                add = True            
                if element == "(":
                    priority += 1
                    if highest_priority == priority:
                        add = False   
                elif element == ")":
                    if highest_priority == priority:
                        add = False 
                    priority -= 1

                if add:
                    cleaned_condition += element
            return cleaned_condition


                

        def matching_value_in_condition(current_condition,highest_priority):
            """
            This function combines two values that are in the highest 
                priority (innermost) parenthesis. 

            Args: current_condition (string) - The current condition that we are
                    evaluating in string form.
                  
                  highest priority - The priority state that he has to combine.

            Returns: to_do_next_loop (string) - This function returns three types
                        of string which are; 
                            * The new current condition -> This is the current
                            condition after two values has been merged.
                            * The string "reduce one" -> This means that the
                            priority is ready to be reduce by one.
                            * The string "done" -> This means that the whole 
                            process is done and a single value has emerged.
            """
            priority = 0
            start_element = 0
            end_element = 0
            first_number = ""
            second_number = ""
            first_done = False
            second_done = False
            have_condition = False
            and_condition = True
            overflow = True 

            index = 0
            for element in current_condition:
                # Evaluate elements
                if element == "(":
                    start_element = index
                    priority += 1
                elif element == ")":
                    
                    priority -= 1
                    if first_done == True and have_condition == True:
                        if have_condition == True:
                            overflow = False
                            second_done = True
                            end_element = index
                            break
                    else:
                        #Reset And Try To Get Another Highest Priority
                        start_element = 0
                        end_element = 0
                        first_number = ""
                        second_number = ""
                        first_done = False
                        second_done = False
                        have_condition = False
                        and_condition = True
                else:
                    if highest_priority == priority:
                        # Filter if it's a value or a condition
                        Value = [
                            '1','2','3','4','5','6','7','8','9','0','.','-'
                        ]

                        Condition = ['a','n','d','o','r']
                        if element != " ":

                            if element in Value:
                                if first_done == False:
                                    first_number += element
                                else:
                                    second_number += element
                            elif element in Condition:
                                if second_done != True:

                                    if element == "a":
                                        and_condition = True
                                        have_condition = True
                                        if first_done == True:
                                            second_done = True
                                        else:
                                            first_done = Truefirst_done = True

                                    elif element == "o":
                                        have_condition = True
                                        if first_done == True:
                                            second_done = True
                                        else:
                                            first_done = True

                                        and_condition = False
                                else:
                                    second_done = True
                                    end_element = index-2
                                    overflow = False
                                    break     
                index += 1

            # If the string suddenly end without setting the overflow to false
            #       set the second_done into true
            if second_number != "" and overflow == True:
                second_done = True
                end_element = index

            merged = False
            # merging
            if first_done == True and second_done == True:
                merged = True
                first_done = False
                second_done = False
                result = 0
                first_number = float(first_number)
                second_number = float(second_number)
                if and_condition == True:
                    result=conjuct_certainty_factors(first_number,second_number)
                else:
                    result=disjunct_certainty_factor(first_number,second_number)

            # Making a new current condition
            to_do_next_loop = ""
            if merged == True:
                ReplaceIndex = 0
                for element in current_condition:
                    if ReplaceIndex < start_element or \
                        ReplaceIndex >= end_element:

                        to_do_next_loop += element
                    elif ReplaceIndex == end_element-1:
                        to_do_next_loop += str(result)
                    ReplaceIndex += 1
                
            else:
                # Removes Parenthesis
                to_do_next_loop=remove_innermost_parenthesis(
                    current_condition,highest_priority)
            if to_do_next_loop == current_condition:
                if highest_priority != -1:
                    to_do_next_loop = "reduce one"
                else:
                    to_do_next_loop = "done"
            return to_do_next_loop   
  
                 

        def evaluate_condition(StringCondition):
            """
                This function evaluates the Condition Order until returns it
                    in a single value

                Args: StringCondition (string) - The condition that is in
                    string form

                Returns: final_value (float) - The final certainty factor of 
                    the disease
            """
            priority = 0
            highest_priority = 0
            # Know the highest priority first
            for element in StringCondition:
                if highest_priority < priority:
                    highest_priority = priority

                if element == "(":
                    priority += 1
                elif element == ")":
                    priority -= 1
            current_condition = StringCondition
            final_value = 0
            while current_condition != "done":
                # Loop until the current_condition says done
                past_condition = current_condition
                current_condition=matching_value_in_condition(
                    current_condition,highest_priority)
                if current_condition == "reduce one":
                    current_condition = past_condition
                    highest_priority -= 1
                elif current_condition == "done":
                    final_value = past_condition

            return float(final_value)

  
        def serialize_question(query_set,hypothesis,progress):
            """
                This function serializes the examining question

                Args: query_set - Query that must be serialized
                      hypothesis - The current hypothesis that the application is
                                    trying to prove

                Returns: data - The data that must be returned to response
            """
            serialized = QuestionSerializer(query_set, many=True)
            data = { 'question': serialized.data , 'result' : 'no', 
                'hypothesis': hypothesis, 'progress' : progress}
            return data

        def scan_disease(to_investigate):
            """
                This function scans the disease to investigate and returns
                    a query set if the disease hasn't completed all the rules.
                    if a disease completed all the rules this will return a 
                    string value of "re,##" which the "re" means recalibration
                    and the following '##' will be the certainty factor,

                Args: to_investigate - This is the 'id' of the disease that we
                                will investigate.

                Returns: next_action - This variable will determine what will be
                            the next action of the server. If it returns a 
                            query set, it will try to ask the question. If it 
                            returns a string, it will recalibrate for the next
                            question. string in this format "re-##".
            """
            next_action = ""
            answered_question = []
            paremters_splitted=parameters.split(',')

            if parameters != "start":
                for splitted_parameter in paremters_splitted:
                    answered_questions_raw_data = splitted_parameter.split('=')
                    answered_question.append(answered_questions_raw_data)
            # Get Target Rules
            try:

                # Makes sure that the target disease is not archived
                target_rules = Rule.objects.filter(
                    archived=False,disease__id=to_investigate,
                    disease__archived=False)
                
                certainty_factor_of_target = 0

                for rule in target_rules:
                    rule_id=rule.id
                    target_evidences = Evidence.objects.filter(
                        evidences__rule__id=rule_id)

                    evidence_id = 0
                    height_strike = len(target_evidences)
                    strike = 0
                    # This variable is used for the condition hierarchy
                    evidence_holder = []

                    recursion_action = ""

                    for evidence in target_evidences:
                        evidence_id = evidence.id
                        for x in range(0,len(answered_question)):
                            if evidence.id == int(answered_question[x][0]):
                                to_insert_in_evidence_holder = [str(answered_question[x][0]), \
                                        str(answered_question[x][1])]
                                evidence_holder.append(
                                    to_insert_in_evidence_holder)
                                evidence_id = 0
                                strike += 1

                                break
                        if evidence_id != 0:
                            do_not_break = False
                            # A rule is not completed - Tries to ask the user the incomplete rule
                            temporary_next_action = Evidence.objects.filter(
                                id=evidence_id,archived=False)

                            next_action_is_string=isinstance(
                                temporary_next_action, basestring)


                            if next_action_is_string == False:
                                if temporary_next_action[0].linked_disease is not None:
                                    # If the evidence is a linked disease, scan that disease
                                    #   for questions. 
                                    recursion_action = scan_disease(
                                        temporary_next_action[0].linked_disease.id)
                                    
                                    if recursion_action:
                                        if isinstance(recursion_action, basestring):
                     
                                            splitted_action = recursion_action.split(',')
                                            

                                            to_insert_in_evidence_holder = [str(evidence_id), \
                                                    str(splitted_action[1])]
                                            evidence_holder.append(to_insert_in_evidence_holder)

                                            strike += 1
                                            evidence_id = 0
                                            do_not_break = True
                                        else:
                                            next_action = recursion_action
                                       
                                else:
                                    next_action = temporary_next_action

                            if do_not_break == False:
                                # Break if the specific rule hasn't been completed
                                break 

                    if evidence_id != 0:
                        # A rule is not yet completed, break the loop and ask a question
                        break
                    elif evidence_id == 0 and height_strike == strike:
                        # The rule is complete calculate calcuate cf 
                        # If condition hierarchy exists
                        premise_total = 0
                        
                        if height_strike > 1:
                            Numbers = ['1','2','3','4','5','6','7','8','9','0']
                            index = 0
                            ID_Detected = ""

                            To_Evaluate_Condition = ""
                            Condition_Order = rule.Condition_Order
                            for character in Condition_Order:
                                
                                if character in Numbers:
                                    ID_Detected += character
                                else:

                                    if ID_Detected != "":
                                        for x in range(0,len(evidence_holder)):
                                            
                                            if ID_Detected == evidence_holder[x][0]:
                                                To_Evaluate_Condition += str(evidence_holder[x][1])
                                    ID_Detected = ""
                                    To_Evaluate_Condition += character
                                index += 1
                                # Evaluates the last element of the string if it's evidence
                                if index == len(Condition_Order):
                                    if ID_Detected != "":
                                        for x in range(0,len(evidence_holder)):
                                            if ID_Detected == evidence_holder[x][0]:
                                                To_Evaluate_Condition += str(evidence_holder[x][1])
                                    ID_Detected = ""
                            # evaluate the existing condition
                            premise_total = evaluate_condition(To_Evaluate_Condition)
                        else:
                            if recursion_action:
                                splitted_action = recursion_action.split(',')
                                premise_total = float(splitted_action[1]) 

                            else:
                                premise_total =int(evidence_holder[0][1])

                        raw_cf = float((rule.certainty_factor * premise_total)) / 100


                        certainty_factor_of_target=combine_multiple_rules_with_the_same_conclusion(
                                certainty_factor_of_target,raw_cf)

                        if certainty_factor_of_target > 0.995 or certainty_factor_of_target < -0.995:
                            # Target Disease already built enough certainty factor
                            return "re," + str(certainty_factor_of_target)

                if next_action == "":
                    next_action = "re," + str(certainty_factor_of_target)

            except Exception as e:
                #Target disease can't be Found
                print str(e)
                next_action = "re,xx"
            return next_action                   

        # Global name space
        decision = ""
        # Backward Chaining Target
        decision = scan_disease(int(target))
        Recalibration=isinstance(decision, basestring)

        if Recalibration:
            #Recalibration
            cf_of_all_disease = {}
            all_disease = Disease.objects.filter(archived=False)
            length_of_all_disease = len(all_disease)
            number_of_disease_completed = 0
            progress = 0
            for disease in all_disease:
                # Get another disease to target if it's available
                return_from_recalibration=scan_disease(disease.id)
                Still_Recalibrate=isinstance(
                    return_from_recalibration, basestring)
                if Still_Recalibrate:
                    number_of_disease_completed += 1
                    # gets the percentage of progress
                    progress = (float(number_of_disease_completed) / length_of_all_disease)*100
                    raw_result=return_from_recalibration.split(',')
                    # Store the disease if it's already complete
                    cf_of_all_disease[disease.id] = {
                            'id': disease.id,
                            'name' : disease.name,
                            'advise': disease.advise,
                            'cf' : float(raw_result[1]),
                            'details': disease.details
                        }
                else:
                    data = serialize_question(
                        return_from_recalibration,
                        disease.id,progress)
                    return Response(data)

            final_data = {};
            # Result
            for disease in cf_of_all_disease:
                # Cut Off is that the certainty factor that is more than 50%
                if cf_of_all_disease[disease]['cf'] > 0.50:

                    final_data[cf_of_all_disease[disease]['id']] = {
                        'name' : cf_of_all_disease[disease]['name'],
                        'advise': cf_of_all_disease[disease]['advise'],
                        'cf' : format(round(cf_of_all_disease[disease]['cf'] * 100,2),'.2f'),
                        'id': cf_of_all_disease[disease]['id'],
                        'details': cf_of_all_disease[disease]['details']
                    }
           
            final_data = json.dumps(final_data)
            json_final_data = json.loads(final_data)
            data = { 'result_item': json_final_data , 'result' : 'yes'}
            return Response(data)

        else:
            data = serialize_question(decision,target,'no change')
            return Response(data)

