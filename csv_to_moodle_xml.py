
import csv
import xml.etree.ElementTree as ET

def csv_to_moodle_xml(file_path):
    quiz = ET.Element("quiz")
    
    with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            if row['Category']:
                category = ET.SubElement(quiz, "question")
                category.set("type", "category")
                text = ET.SubElement(category, "category")
                ET.SubElement(text, "text").text = f"$course$/top/{row['Category']}"
            
            question = ET.SubElement(quiz, "question")
            
            images_md = ""
            if 'Image URLs' in row and row['Image URLs']:
                image_urls = row['Image URLs'].split(';;')
                images_md = "\n".join([f"![Image]({url.strip()})" for url in image_urls])
            
            if row['Question Type'].upper() == "NUM":
                question.set("type", "numerical")
                ET.SubElement(question, "name").text = row['Question Text']
                ET.SubElement(question, "questiontext").text = f"{row['Question Text']}\n{images_md}"
                ET.SubElement(question, "defaultgrade").text = row['Points']
                ET.SubElement(question, "feedback").text = row['Feedback']
                
                answer = ET.SubElement(question, "answer")
                answer.set("fraction", "100")
                ET.SubElement(answer, "text").text = row['Correct Answer']
                
                if 'Tolerance Value' in row and row['Tolerance Value']:
                    tolerance_type = row.get('Tolerance Type', 'Nominal').upper()
                    tolerance_value = row['Tolerance Value']
                    if tolerance_type == "RELATIVE":
                        # Calculate relative tolerance
                        tolerance = float(row['Correct Answer']) * (float(tolerance_value.strip('%')) / 100)
                    else:
                        # Use nominal tolerance
                        tolerance = float(tolerance_value)
                    
                    ET.SubElement(answer, "tolerance").text = str(tolerance)
            
            # ... [rest of the logic for MC, TF, and SA questions as in the previous script]
                    
    return ET.tostring(quiz, encoding="utf-8", method="xml").decode("utf-8")

# ... [rest of the script for command-line execution as before]
