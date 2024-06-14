import xml.etree.ElementTree as ET
from lxml import etree
import os

# Load and parse the XML plan


# Function to extract join order and join types
def extract_joins(root):
    joins = []
    tables=[]
    for plan_node in root.iter("{http://www.postgresql.org/2009/explain}Plan"):
        head = plan_node.find("{http://www.postgresql.org/2009/explain}Node-Type").text
        if "Scan" in head:
         if "Bitmap Index" in head:
           continue
         r = plan_node.find("{http://www.postgresql.org/2009/explain}Relation-Name").text
         
         
         tables.append(r)
 
        if(head=="Hash Join"):
         c=plan_node.find("{http://www.postgresql.org/2009/explain}Hash-Cond").text
         c=c.strip('()')
         left_side, right_side = c.split('=')
         s1 = left_side.split('.')[0].strip()
         s2 = right_side.split('.')[0].strip()
         joins.append('HashJoin('+s1 +" "+s2+")")
        elif(head=="Merge Join"):
         c=plan_node.find("{http://www.postgresql.org/2009/explain}Merge-Cond").text
         c=c.strip('()')
         left_side, right_side = c.split('=')
         s1 = left_side.split('.')[0].strip()
         s2 = right_side.split('.')[0].strip()
         joins.append('MergeJoin('+s1 +" "+s2+")")
        
    
         
        elif(head=="Nested Loop"):f1
         if(plan_node.find("{http://www.postgresql.org/2009/explain}Join-Filter") is not None):
    
          c=plan_node.find("{http://www.postgresql.org/2009/explain}Join-Filter").text
          c=c.strip('()')
          left_side, right_side = c.split('=')
          s1 = left_side.split('.')[0].strip()
          s2 = right_side.split('.')[0].strip()
          joins.append('NestLoop('+s1 +" "+s2+")")
      
    return joins,tables

# Function to extract table names and join conditions
def extract_tables_and_conditions(root):
    tables = []
    order=[]
    conditions = []
    for plan_node in root.iter("{http://www.postgresql.org/2009/explain}Plan"):
        
        head = plan_node.find("{http://www.postgresql.org/2009/explain}Node-Type").text
        
        if"Scan" in head:
         if "Seq" in head:
           r = plan_node.find("{http://www.postgresql.org/2009/explain}Relation-Name").text
           tables.append("SeqScan"+"("+r+")")
         
         
           
         elif "Index Scan" in head:
           if "Bitmap Index" in head:
             continue
           
           r = plan_node.find("{http://www.postgresql.org/2009/explain}Relation-Name").text
         
           tables.append("IndexScan"+"("+r+" "+r+"_pkey"+")")
         else:
           
           
             r = plan_node.find("{http://www.postgresql.org/2009/explain}Relation-Name").text
         
             tables.append("BitmapScan"+"("+r+" "+r+"_pkey"+")")
             
           
         
         
         
         
         
         
    # for hash_cond in root.iter('Hash-Cond'):
    #     conditions.append(hash_cond.text)
    return tables, conditions

# Extract information from the XML plan
 

# Construct the query with pg_hint constructs
folder_path="/home/haris/output_xml_files"

for file_name in os.listdir(folder_path):
 plan_path = os.path.join(folder_path, file_name)
 
 xml = etree.parse(plan_path)
 root = xml.getroot()
 joins,order= extract_joins(root)
 tables, conditions = extract_tables_and_conditions(root)

 hints = ' '.join(joins) + ' ' + ' '.join(tables) +' '+"Leading("+' '.join(order)+")"
 query = f"/*+ {hints} */\n explain Analyze SELECT MIN(company_name.name) AS from_company,MIN(link_type.link)" \
        "AS movie_link_type,MIN(title.title) AS non_polish_sequel_movie FROM " \
        "company_name ,company_type ,keyword ,link_type ,movie_companies ,movie_keyword ,movie_link ,title WHERE company_name.country_code !='[pl]' AND (company_name.name LIKE '%Film%' OR company_name.name LIKE " \
        "'%Warner%') AND company_type.kind ='production companies' AND keyword.keyword ='sequel' AND link_type.link LIKE '%follow%' AND movie_companies.note IS NULL AND title.production_year BETWEEN 1950 AND " \
        "2000 AND link_type.id = movie_link.link_type_id AND movie_link.movie_id = title.id AND title.id = movie_keyword.movie_id AND movie_keyword.keyword_id = keyword.id AND title.id = " \
        "movie_companies.movie_id AND movie_companies.company_type_id = company_type.id AND movie_companies.company_id = company_name.id AND movie_link.movie_id = movie_keyword.movie_id AND movie_link.movie_id" \
        "= movie_companies.movie_id AND movie_keyword.movie_id = movie_companies.movie_id;"
 output_dir = '/home/haris/query_files'
 # Ensure the output directory exists
 if not os.path.exists(output_dir):
    os.makedirs(output_dir)
 output_file_path = os.path.join(output_dir, os.path.splitext(file_name)[0] + '.sql')
 with open(output_file_path, 'w') as output_file:
            output_file.write(query)


print("Processing complete.")

#print(query)

