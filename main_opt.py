from Algorithm.GA_nn.algorithm.GA import GA
import numpy as np
from Game.game import BaseGameRule


game = BaseGameRule()
all_w = [np.random.rand(60, 3), np.random.rand(3, 1)]
all_b = [np.random.rand(3, 1), np.random.rand(1, 1)]


# 定义适应度函数：每次游戏结束后返回得分，设置子弹惩罚
def problem(gene):
    characteristics = gene
    default = [all_w, all_b]
    players = {
        'names': ['p1', 'p2'],
        'teams': ['red', 'blue'],
        'characteristics': [characteristics, default],
    }
    fit_lst = []
    # 每一个人循环100次随机条件，求平均分，反映其应对不同情况的能力。
    for i in range(100):
        game.restart_game(players)
        for i in range(100):
            game.step()
        fitness = game.get_result()['p1']
        game.game_over()
        fit_lst.append(fitness)
    ave_fit = sum(fit_lst)/100
    print(ave_fit)
    return ave_fit/100


if __name__ == '__main__':
    n_input = 60
    n_neurons_1 = 1
    n_output = 1

    gene_num = [n_input+1 for i in range(n_neurons_1)]
    gene_num.append(n_neurons_1+1)

    problem([all_w, all_b])
    ga = GA(problem, n_neurons_1+n_output, [], gene_num=gene_num, n_generations=10, population_size=100)
    ga.run()
    characteristics = ga.get_result()
    # 保存特征数组为文件
    np.save('./datas/all/all_w_0.npy', characteristics[0][0])
    np.save('./datas/all/all_w_1.npy', characteristics[0][1])
    np.save('./datas/all/all_b_0.npy', characteristics[1][0])
    np.save('./datas/all/all_b_1.npy', characteristics[1][1])
