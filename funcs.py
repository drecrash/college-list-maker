import json

def get_data():
    with open("data.json","r") as f:
        user = json.load(f)

    return user

def get_ec_data():
    with open("ecs.json","r") as f:
        user = json.load(f)

    return user

def get_importance_data():
    with open("ecimportance.json","r") as f:
        user = json.load(f)

    return user

# taken from geekforgeeks and favtutor
def sort_dict(thedict):
    fin_dict = dict(sorted(thedict.items(), key=lambda item: item[1], reverse=True))
    
    return fin_dict


def main(user_gpa, user_testoptional, chosen_test, user_actscore, user_satscore, user_income, user_essayskills, user_ecs):
    all_universities = ["Arizona State University", "Boston University", "Carnegie Mellon University", "Columbia", "Cornell", "Duke University", "Georgetown University", "Georgia Institute of Technology", "Harvard", "Indiana University Bloomington", "Johns Hopkins University", "Michigan State University", "New York University", "North Carolina State University", "Northwestern University", "Penn State University", "Princeton", "Purdue University", "Stanford", "Texas A&M University", "The Ohio State University", "Tufts University","University of California Davis", "University of California Irvine", "University of California Los Angeles", "University of California San Diego", "University of Chicago", "University of Colorado Boulder", "University of Florida", "University of Maryland", "University of Michigan", "University of Minnesota", "University of Pennsylvania", "University of Southern California", "University of Texas Austin","University of Wisconsin Madison", "Yale"]
    uni_dict = {}
    data = get_data()
    ec_data = get_ec_data()
    importance_data = get_importance_data()
    # percentage of income spent on college
    income_spent = 0.47

    for i in range(len(all_universities)):
        uni_dict[all_universities[i]] = 5


    for i in range(len(all_universities)):
        if float(data[all_universities[i]]["Testing"]["AvgGPA"]) > user_gpa + 1:
            uni_dict[all_universities[i]] -= 1

        if float(data[all_universities[i]]["Testing"]["AvgGPA"]) > user_gpa + 2:
            uni_dict[all_universities[i]] -= 2

        if float(data[all_universities[i]]["Testing"]["AvgGPA"]) >= user_gpa + 3:
            uni_dict[all_universities[i]] -= 2

        if float(data[all_universities[i]]["Testing"]["AvgGPA"]) < user_gpa:
            uni_dict[all_universities[i]] += 1


    if user_testoptional == False:


        if chosen_test == "A":
            for i in range(len(all_universities)):
                uni = all_universities[i]
                try:
                    if data[uni]["Testing"]["LowACT"] != []:
                        if int(data[uni]["Testing"]["LowACT"][2]) > user_actscore:
                            uni_dict[uni] -= 1

                            if int(data[uni]["Importance"]["Standardized"]) <= 2:
                                uni_dict[uni] -= 1

                        else:
                            if int(data[uni]["Testing"]["MidACT"][2]) > user_actscore:

                                if int(data[uni]["Importance"]["Standardized"]) <= 2:
                                    uni_dict[uni] -= 1

                            else:
                                if int(data[uni]["Testing"]["TopACT"][2]) > user_actscore:
                                    pass
                                else:
                                    uni_dict[uni] += 1  

                                    if int(data[uni]["Testing"]["TopACT"][2]) + 3 <= user_actscore:
                                        if int(data[uni]["Importance"]["Standardized"]) <= 2:
                                            uni_dict[uni] += 1
                
                except:
                    print(f"ACT Error on {uni}")
                    continue


        else:
            for i in range(len(all_universities)):
                uni = all_universities[i]
                try:
                    if data[uni]["Testing"]["LowSAT"] != []:
                        if int(data[uni]["Testing"]["LowSAT"][2]) > user_satscore:
                            uni_dict[uni] -= 1

                            if int(data[uni]["Importance"]["Standardized"]) <= 2:
                                uni_dict[uni] -= 1

                        else:
                            if int(data[uni]["Testing"]["MidSAT"][2]) > user_satscore:

                                if int(data[uni]["Importance"]["Standardized"]) <= 2:
                                    uni_dict[uni] -= 1

                            else:
                                if int(data[uni]["Testing"]["TopSAT"][2]) > user_satscore:
                                    pass
                                else:
                                    uni_dict[uni] += 1  

                                    if int(data[uni]["Testing"]["TopSAT"][2]) + 100 <= user_satscore:
                                        if int(data[uni]["Importance"]["Standardized"]) <= 2:
                                            uni_dict[uni] += 1

                except:
                    print(f"SAT Error on {uni}")
                    continue



    else:
        for i in range(len(all_universities)):
            uni = all_universities[i]

            if data[uni]["Testing"]["Optional"] == False:
                uni_dict[uni] = -100



    user_aid = False   

    if user_income < 90000:
        user_aid = True



    

    for i in range(len(all_universities)):
        uni = all_universities[i]

        if user_essayskills >= 4 and int(data[uni]["Importance"]["Essay"]) <= 2:
            uni_dict[uni] += 1

        elif user_essayskills <= 3 and int(data[uni]["Importance"]["Essay"]) <= 2:
            uni_dict[uni] -= 1
    
        elif user_essayskills <= 2:
            uni_dict[uni] -= 1


    total_ec_importance = 0
    for i in range(len(all_universities)):
        uni = all_universities[i]
        uni_ecs = list(ec_data[uni].keys())
        for i in range(len(user_ecs)):
            current_ec = user_ecs[i]

            if current_ec in uni_ecs:
                if ec_data[uni][current_ec] <= 2:
                    uni_dict[uni] += (ec_data[uni][current_ec] + importance_data[current_ec])
                else:
                    uni_dict[uni] += (ec_data[uni][current_ec])

                total_ec_importance += importance_data[current_ec]


        for i in range(len(uni_ecs)):
            if uni_ecs[i] not in user_ecs:
                if ec_data[uni][uni_ecs[i]] >= 3:
                    uni_dict[uni] -= (ec_data[uni][uni_ecs[i]] + importance_data[uni_ecs[i]])
                else:
                    uni_dict[uni] -= ec_data[uni][uni_ecs[i]]

    uni_dict_keys = list(uni_dict.keys())

    if len(user_ecs) <= 9 and (total_ec_importance < 24):
        for i in range(len(uni_dict_keys)):
            uni_dict[uni_dict_keys[i]] -= 1


    if (user_income > 100000) and (total_ec_importance < 20):
        for i in range(len(uni_dict_keys)):
            uni_dict[uni_dict_keys[i]] -= 2

    if (user_income < 80000) and (total_ec_importance > 32):
        for i in range(len(uni_dict_keys)):
            uni_dict[uni_dict_keys[i]] += 2
    

    else:
        for i in range(len(all_universities)):
            uni = all_universities[i]
            total_tuition = int(str(data[uni]["Finances"]["Tuition"]).replace(',', '')) + int(str(data[uni]["Finances"]["RoomBoard"]).replace(',', ''))
            if user_aid:
                total_tuition -= int(str(data[uni]["Finances"]["AvgAid"]).replace(',', ''))

            if (user_income*income_spent) < total_tuition:
                uni_dict[uni] -= 2

            elif (user_income*income_spent) < total_tuition/3:
                uni_dict[uni] -= 2     

            elif (user_income*income_spent) > (total_tuition * 1.5):
                uni_dict[uni] += 1

    uni_dict = sort_dict(uni_dict)

    
    amount_printed = 0
    uni_dict_keys = list(uni_dict.keys())
    print("You should apply to the following top schools:")
    final_string = ""
    for i in range(5):
        if uni_dict[uni_dict_keys[i]] >= 5:
            if i != 5:
                final_string += f"{uni_dict_keys[i]}, "
            else:
                final_string += f"{uni_dict_keys[i]}"

            amount_printed += 1

    if amount_printed == 0:
        final_string = "Apologies, but we couldn't find any top schools that would meet your criteria"

    return final_string
