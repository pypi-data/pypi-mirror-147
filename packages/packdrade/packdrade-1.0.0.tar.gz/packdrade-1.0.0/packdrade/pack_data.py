import pandas as pd


class Utilities():

    def create_data(df_target, name_column, list_keys, name_df='df'):
        """
        1. verifique em cada linha do dataframe se existe a palavra de busca
        2. se a palavra existir, adicione na linha de outro dataframe
        3. se não existir, continuar a busca até finalizar
        4. no final o resultado deve ser um data frame apenas com os valores encontrados
        """
        name_df = pd.DataFrame(columns=df_target.columns)
        for item in enumerate(list_keys):
            data = df_target.loc[df_target[name_column] == item[1]]
            count = 0
            while count < len(data.values):
                name_df.loc[len(name_df)+1] = data.values[count]
                count += 1
        return name_df

    def word_serach(col_target, word_list=None, word=None):
        """
        Essa função não retorna nenhum valor no momento.
        Utilize-a para verificar se determinada palavra é encontrada na coluna alvo
        """
        if word == None and word_list == None:
            return 'Nenhum valor passado'
        if type(word) != list and type(word) == str:
            forlist = [word]
        if word_list != None:
            forlist = word_list

        col_target = set(col_target)
        for item in forlist:
            if item.capitalize() in col_target:
                print(item.capitalize(), 'encontrado')
            elif item in col_target:
                print(item, 'encontrado')
            else:
                print(item.capitalize(), 'não encontrado')
