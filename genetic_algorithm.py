import random

#初期個体生成
def generate_initial_population (amount) :
    first_list = []
    for i in range(amount) :
        a = random.randint(1,5)
        b = random.randint(1,5)
        first_list.append((str(a), str(b)))
    #print("初期個体" + str(first_list))
    return first_list

#個体評価
def evaluation (amount, list) :
    eval_list = []
    def calculate (a,b): 
        return a*(10-a)*b*(8-b)
    for i in range(amount) :
        a = int(list[i][0])
        b = int(list[i][1])
        score = calculate(a,b)
        #print("個体" + str(list[i]) + "の評価値は" + str(score))
        eval_list.append((list[i], score))
    return eval_list

#選択・自然淘汰
def selection (survive, eval_list) :
    sorted_list = sorted(eval_list, key=lambda x: x[1], reverse=True)
    survived_gen = [gene for gene, _ in sorted_list[:survive]]
    #print("生き残った個体" + str(survived_gen))
    return survived_gen

#交叉(AIが作った部分)
def crossover (survived_gen, amount) :
    next_gen = []
    while len(next_gen) < amount :
        parent1 = random.choice(survived_gen)
        parent2 = random.choice(survived_gen)
        cross_point = random.randint(1,1)
        child = parent1[:cross_point] + parent2[cross_point:]
        next_gen.append(child)
    #print("次世代の個体" + str(next_gen))
    return next_gen

#評価値付きで表形式表示する関数
def display_table_with_fitness(generation_data):
    """
    個体を行、世代を列にして、評価値も含めて表形式で表示
    generation_data: [(世代番号, [(個体, 評価値), ...]), ...]
    """
    if not generation_data:
        return
    
    # 各世代の個体を評価値の降順でソート
    sorted_generation_data = []
    for gen_num, individuals in generation_data:
        sorted_individuals = sorted(individuals, key=lambda x: x[1], reverse=True)
        sorted_generation_data.append((gen_num, sorted_individuals))
    
    # 個体数と世代数を取得
    max_individuals = max(len(individuals) for _, individuals in sorted_generation_data)
    num_generations = len(sorted_generation_data)
    
    # ヘッダー行を作成（世代を列として表示）
    header = "個体\\世代\t"
    for gen_num, _ in sorted_generation_data:
        header += f"世代{gen_num}\t\t"
    print(header.rstrip('\t'))
    print("=" * (8 + num_generations * 20))
    
    # 各個体のデータを表示（個体ごとに行を作成）
    for i in range(max_individuals):
        row = f"個体{i+1}\t\t"
        for _, individuals in sorted_generation_data:
            if i < len(individuals):
                individual, fitness = individuals[i]
                row += f"{individual}({fitness})\t"
            else:
                row += "\t"
        print(row.rstrip('\t'))
    print()

#メイン処理
def main():
    print()
    generation = int(input("世代数を入力してください:"))
    amount = int(input("個体数を入力してください:"))
    survive = int(input("選択・自然淘汰で生き残る個体数を入力してください:"))
    
    # 全世代のデータを保存
    all_generations_with_fitness = []
    
    current_list = generate_initial_population(amount)
    
    for gen in range(generation):
        eval_list = evaluation(amount, current_list)

        # 世代データを保存（評価値付き）
        all_generations_with_fitness.append((gen, eval_list))
        
        survived_gen = selection(survive, eval_list)
        current_list = crossover(survived_gen, amount)
    
    # 最終世代も追加
    eval_list = evaluation(amount, current_list)
    all_generations_with_fitness.append((generation, eval_list))
    
    # 表形式で全世代を表示
    print("\n" + "="*60)
    print("【全世代の個体と評価値一覧表】")
    print("="*60)
    display_table_with_fitness(all_generations_with_fitness)
    
    # 個体の割合を表示
    print("\n最終世代の個体の割合:")
    individual_count = {}
    for individual, _ in eval_list:
        if individual not in individual_count:
            individual_count[individual] = 0
        individual_count[individual] += 1
    
    # 割合順にソート
    sorted_count = sorted(individual_count.items(), key=lambda x: x[1], reverse=True)
    for individual, count in sorted_count:
        percentage = (count / amount) * 100
        print(f"{individual}: {count}個体 ({percentage:.1f}%)")

#実行部分
if __name__ == "__main__":
    main()
