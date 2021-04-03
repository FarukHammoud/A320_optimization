import pickle

def switch_lin_to_real(lin,nb_row,nb_column):
    column=lin%nb_column
    if column==0:
        column=nb_column
        row=lin//nb_column
    else:
        row=lin//nb_column+1

    real=(column,row) #colonne, rangée
    return real

def export_dynamic(instance, nb_passengers, nb_places, nb_rows, nb_columns, E, passengers, order, compatible):

        result = {}
        p_matrix = [[None for column in range(6)] for row in range(30) ]
        for pa in range(1,nb_passengers+1): # passagers
            for pl in range(1,nb_places+1): # places
                if E[(pa,pl)].x:
                    column, row = switch_lin_to_real(pl,nb_rows,nb_columns)
                    if column <= 3:
                        p_matrix[row-1][column-1] = {'group':passengers[pa]["Groupe"],'weight':passengers[pa]["Poids"]}
                    else:
                        p_matrix[row-1][column-2] = {'group':passengers[pa]["Groupe"],'weight':passengers[pa]["Poids"]}

        result['p_matrix'] = p_matrix
        result['order'] = order
        result['compatible'] = compatible
        save_obj(result,'result_'+str(instance))

def export_static(instance, nb_passengers, nb_places, nb_rows, nb_columns, E, passengers, order, compatible):
    result = {}
    p_matrix = [[None for column in range(6)] for row in range(30) ]
    for pa in range(1,nb_passengers+1): # passagers
        for pl in range(1,nb_places+1): # places
            if E[(pa,pl)].x:
                column, row = switch_lin_to_real(pl,nb_rows,nb_columns)
                if column <= 3:
                    p_matrix[row-1][column-1] = {'group':passengers[pa]["Groupe"],'weight':passengers[pa]["Poids"]}
                else:
                    p_matrix[row-1][column-2] = {'group':passengers[pa]["Groupe"],'weight':passengers[pa]["Poids"]}

    result['p_matrix'] = p_matrix
    save_obj(result,'result_'+str(instance))

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

