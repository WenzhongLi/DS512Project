#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@author: li
'''
import Formation


class Predict(object):
    # init
    def __init__(self,team1, team2, formation1, formation2):  # team1[11], team2[11], formation1, formation
        self.team1 = team1
        self.team2 = team2
        self.formation1 = formation1
        self.formation2 = formation2

    def Predict(self):
        count_total = 0
        for j in range(0,10):
            count_total += self.team1[j]
        team1_rounds = count_total / 100

        count_total = 0
        for j in range(0, 10):
            count_total += self.team2[j]
        team2_rounds = count_total / 100

        f = Formation.Formation(self.formation1[0], self.formation1[1], self.formation1[2], self.formation2[0],
                                self.formation2[1], self.formation2[2])
        f.set_player(self.team1, self.team2)
        r1 = f.get_Team1()
        r2 = f.get_Team2()
        dbt1 = self.Binomial_Distribution(r1, team1_rounds)
        dbt2 = self.Binomial_Distribution(r2, team2_rounds)
        # full result
        # TODO print matrix
        t1win = float(0)
        t2win = float(0)
        t1t2even = float(0)
        for i in range(0, len(dbt1)):
            for j in range(0, len(dbt2)):
                if i > j:
                    t1win += dbt1[i]*dbt2[j]
                elif i < j:
                    t2win += dbt1[i]*dbt2[j]
                else:
                    t1t2even += dbt1[i]*dbt2[j]

        print "t1win", t1win, "t2win", t2win, "t1t2even", t1t2even
        # expect
        expect1 = float(0)
        for i in range(0, len(dbt1)):
            expect1 += float(i) * dbt1[i]
        expect2 = float(0)
        for i in range(0, len(dbt2)):
            expect2 += float(i) * dbt2[i]

        print "expect1:", expect1, "expect2:", expect2,

    def Binomial_Distribution(self, p, n):  # Binomial Distribution
        result = []
        for j in range(0,n+1):
            p_k_true = float(0)
            p_k_false = float(0)
            for k in range(0,j+1):
                if p_k_true == 0:
                    p_k_true = p
                else:
                    p_k_true = p * p_k_true
            for k in range(j,n+1):
                if p_k_false == 0:
                    p_k_false = (1-p)
                else:
                    p_k_false = (1-p) * p_k_false
            upper = 1
            below = 1
            for i in range(n - j +1, n+1):
                upper = upper * i
            for i in range(1, j+1):
                below = below * i

            result.append(float(upper/below) * p_k_true * p_k_false)

        #print result
        # normalization
        count = float(0)
        for r in result:
            count += r
        for i in range(0, len(result)):
            result[i] = result[i] / count
        print result
        return result


if __name__ == "__main__":
    predict = Predict([90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90], [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90],
            [4, 4, 2], [4, 5, 1])
    # predict.Binomial_Distribution(0.2, 10)
    predict.Predict()

    predict = Predict([90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90], [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90],
                      [4, 4, 2], [4, 4, 2])
    predict.Predict()

    predict = Predict([94, 86, 89, 90, 85, 89, 87, 90, 85, 84, 85], [82, 92, 93, 87, 87, 86, 85, 83, 87, 76, 85],
                      [4, 3, 3], [4, 3, 3])
    # Real Madrid starting XI: Keylor Navas; Achraf, Varane, Ramos, Marcelo;
    #  Modrić, Kroos, Isco; Bale,  Benzema, Ronaldo.
    # Barcelona Starting XI: Ter Stegen; Vidal, Pique, Umtiti, Alba;
    #  Busquets, Rakitic, Iniesta; Messi, Suarez, Deulofeu.

    predict.Predict()
    # predict = Predict([90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90], [85, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85],
    #                   [4, 5, 1], [4, 5, 1])
    # predict.Predict()
    #
    # predict = Predict([90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90], [80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80],
    #                   [4, 5, 1], [4, 5, 1])
    # predict.Predict()
    #
    # predict = Predict([90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90], [70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70],
    #                   [4, 5, 1], [4, 5, 1])
    # predict.Predict()
    #
    # predict = Predict([90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90], [55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55],
    #                   [4, 5, 1], [4, 5, 1])
    # predict.Predict()

    # predict = Predict([90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90], [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90],
    #                   [4, 4, 2], [4, 4, 2])
    # predict.Predict()

    # f = Formation.Formation(1, 5, 4, 1, 5, 4)
    # f.set_player([90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90], [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90])
    # f.get_Team1()
    # f.get_Team2()
    #
    # f = Formation.Formation(4, 4, 2, 4, 4, 2)
    # f.set_player([90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90], [85, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85])
    # f.get_Team1()
    # f.get_Team2()


# Input: Data of a given teams team1[11], team2[11], formation for both team formation 1, formation 2.
# Output: The possibility prediction  of match result.
'''
getlocalpossibility(team1[11], team2[11], formation1, formation2)
Team1fowardNetwork = []
Team2fowardNetwork = []
Team1fowardNetwork[0] = 1 # goal
   keeper
Team2fowardNetwork[0] = 1 # goal
   keeper
for order of team1network
Team1fowardNetwork[i] = general influence from all the predecessor;
# this could vary for different position.
for order of team1network
Team1fowardNetwork[i] = general influence from all the predecessor;
# this could vary for different position.
Team1score = matchroundconstant *
Team1fowardNetwork[10]
Team2score = matchroundconstant *
Team1fowardNetwork[10]
Team1scoreresult =
Gaussiandistribution(Team1score)
Team2scoreresult =
Gaussiandistribution(Team2score)
# generate match result possibility
chart
by
crossmatching
for i in Team1scoreresult:
    for j In Team2scoreresult: resultchart[i][j] = (
        Team1scoreresult[i],
        Team1scoreresult[j])
    return resultchart
getlocalpossibility(team1[11], team2
[11], formatio1, formatio2):
for formation1, formation2 in different location:
    possibilityQueue[i] =
    localpossibility(
        team1PlayersAtThisLocation,
        team2PlayersAtThisLocation
        , location)
localpossibility(team1players[],
                 team2players[], location)
# for dfferent location will
consider
different
player
status
team1value = sum
of
certain
player
status + log(constant * (1 +
                         player))
team2value = sum
of
certain
player
status + log(constant * (1 +
                         player))
return team1value / (team1value +
                     team2value);
'''