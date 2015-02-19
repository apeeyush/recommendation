infile='22/22UpdatedData'
outfile='22/transformedData'
parameter_list = ['product_description', 'Type', 'Fabric', 'Wash Care', 'Fit', 'Color', 'SKU', 'Sleeves', 'Neck', 'Length', 'Style', 'Package Contents', 'Material', 'Product Dimensions', 'Fabric Details']

with open(infile) as infile:
    with open(outfile,'a') as outfile:
#        # Get parameters list
#        for line in infile:
#            components = line.split(';')
#            for component in components:
#                if component.find(':') > 0 and component.find('http') < 0:
#                    parts = component.split(':')
#                    if parts[0] not in parameter_list:
#                        parameter_list.append(parts[0])
#        print parameter_list

        # Transform Data
        outfile.write('url, brand, ')
        for parameter in parameter_list:
            outfile.write(parameter+',')
        outfile.write('\n')
        for line in infile:
            components = line.split(';')
            outfile.write(components[0].replace(',',"")+','+components[1].replace(',',"")+',')
            for parameter in parameter_list:
                for component in components:
                    if component.find(':') >= 0 and component.find('http') < 0 and component.find(parameter)>=0:
                        outfile.write(component.split(':')[1].replace(',',""))
                outfile.write(',')
            outfile.write('\n')
