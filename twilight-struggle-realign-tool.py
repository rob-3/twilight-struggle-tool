my_player_influence = int(input("How much influence do you have in the target country? "))
my_opp_influence = int(input("How much influence does your opponent have in the target country? "))
my_modifier = int(input("What modifier are you at? "))
my_ops = int(input("How many ops will be used for this realignment? "))


class Scenario:
    def __init__(self, player_influence, opp_influence, modifier, ops):
        self.player_influence = player_influence
        self.opp_influence = opp_influence
        self.modifier = modifier
        self.ops = ops

class Info:
    def __init__(self, opp_loss_distribution, player_loss_distribution):
        self.opp_loss_distribution = opp_loss_distribution
        self.player_loss_distribution = player_loss_distribution

def analyze(scenario):

    # run numbers for realignments
    raw_info = run_realignments(scenario)

    opp_leading_value = 0
    for index in range(len(raw_info.opp_loss_distribution)):
        if raw_info.opp_loss_distribution[index] != 0:
            opp_leading_value = index
            break
    player_leading_value = 0
    for index in range(len(raw_info.player_loss_distribution)):
        if raw_info.player_loss_distribution[index] != 0:
            player_leading_value = index
            break

    final_opp_percents = [i * 100 for i in raw_info.opp_loss_distribution if i != 0]
    final_player_percents = [i * 100 for i in raw_info.player_loss_distribution if i != 0]

    final_opp_distribution = {}
    for index in range(len(final_opp_percents)):
        final_opp_distribution[opp_leading_value + index] = round(final_opp_percents[index], 2)
    final_player_distribution = {}
    for index in range(len(final_player_percents)):
        final_player_distribution[player_leading_value + index] = round(final_player_percents[index], 2)

    info = Info(final_opp_distribution, final_player_distribution)

    print_analysis(info)


def print_analysis(info):
    print()
    print("Opponent's Loss Distribution:")
    for key in info.opp_loss_distribution:
        print(f"{key}: {info.opp_loss_distribution[key]}%")
    print()
    print("Your Loss Distribution")
    for key in info.player_loss_distribution:
        print(f"{key}: {info.player_loss_distribution[key]}%")


def run_realignments(scenario):
    player_influence = scenario.player_influence
    opp_influence = scenario.opp_influence
    modifier = scenario.modifier
    final_opp_distribution = []
    final_player_distribution = []
    for i in range(101):
        final_opp_distribution.append(0)
        final_player_distribution.append(0)

    for player_roll in range(1, 7):
        for opp_roll in range(1, 7):
            effect = (player_roll - opp_roll + modifier)
            if effect < 0 and -effect > player_influence:
                effect = -player_influence
            elif effect > 0 and effect > opp_influence:
                effect = opp_influence

            if effect > 0:
                new_opp_influence = opp_influence - effect
                new_player_influence = player_influence
            elif effect < 0:
                new_player_influence = player_influence + effect
                new_opp_influence = opp_influence
            else:
                new_opp_influence = opp_influence
                new_player_influence = player_influence

            if scenario.ops != 1:
                new_scenario = Scenario(new_player_influence, new_opp_influence, modifier, scenario.ops - 1)

                my_info = run_realignments(new_scenario)

                normalized_opp_distribution = [i / 36 for i in my_info.opp_loss_distribution]
                normalized_player_distribution = [i / 36 for i in my_info.player_loss_distribution]

                if effect > 0:
                    for i in range(effect):
                        normalized_opp_distribution = normalized_opp_distribution[:-1]
                        normalized_opp_distribution.insert(0, 0)
                else:
                    for i in range(-effect):
                        normalized_player_distribution = normalized_player_distribution[:-1]
                        normalized_player_distribution.insert(0, 0)

                final_player_distribution = [x + y for x, y in zip(normalized_player_distribution, final_player_distribution)]
                final_opp_distribution = [x + y for x, y in zip(normalized_opp_distribution, final_opp_distribution)]
            else:
                if effect >= 0:
                    final_opp_distribution[effect] += (1/36)
                    final_player_distribution[0] += (1/36)
                else:
                    final_player_distribution[-effect] += (1/36)
                    final_opp_distribution[0] += (1/36)

    # post processing
    return Info(final_opp_distribution, final_player_distribution)


my_scenario = Scenario(my_player_influence, my_opp_influence, my_modifier, my_ops)
analyze(my_scenario)
