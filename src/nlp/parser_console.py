from class_spatial_query import SpatialQuery

if __name__ == '__main__':
#     s_lst = ["show me cities that are within 10 miles of Dublin and 5 miles of Columbus"
# ]
#     for s in s_lst:
#         SpatialQuery.answer(s)
#         print '----------------------------------------\n'
#         raw_input('next...')
    while(1):
        s=raw_input('\nGive a question:\n')
        SpatialQuery.answer(s)
        
