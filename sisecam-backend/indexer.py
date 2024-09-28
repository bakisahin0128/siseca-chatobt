from datetime import datetime

import pdfminer
import uvicorn
from azure.storage.blob import BlobServiceClient
import zipfile
import tempfile

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from config import app_logger
import math
import json
import os
from config import BLOB_STORAGE_CONFIG
from utils.utils import parse_pdf_with_path, split_text_to_chunks, split_pdf_to_chunks, get_embedding, format_date_as_odatav4
from utils.search import create_index, does_index_exists, ingest_chunks, delete_index, check_document_existence_by_title_and_date


def get_meta_data(directory_path, website_name, file_name, keyword, notified_date):
    """
    Generates metadata for regulation files located in a specific directory path.

    Args:
        directory_path (str): The path to the directory containing files.
        website_name (str): The name of the website associated with the regulation files.
        file_name (str): The name of the file to extract metadata from.
        keyword (str): The keyword to associate with the regulation files.
        notified_date (str): The notified date to include in the metadata.

    Returns:
        metadata_dict (Dict): A dictionary containing the generated metadata.
    """
    metadata_dict = {}
    try:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                if file.startswith('metadata') and file_path.endswith('.json'):
                    with open(file_path, 'r') as f:
                        metadata_dict = json.load(f)

        metadata_dict["website"] = website_name

        if metadata_dict.get("name") is None \
                or (isinstance(metadata_dict.get("name"), float) and math.isnan(metadata_dict.get('name'))) \
                or metadata_dict.get('name') == 'nan' or metadata_dict.get('name') == '':
            metadata_dict["name"] = file_name[11:]

        metadata_dict["title"] = metadata_dict.pop("name")

        if metadata_dict.get("keyword") is None \
                or (isinstance(metadata_dict.get("keyword"), float) and math.isnan(metadata_dict.get('keyword'))) \
                or metadata_dict.get('keyword') == 'nan' or metadata_dict.get('keyword') == '':
            metadata_dict["keyword"] = keyword

        if metadata_dict.get("notified_date") is None \
                or (isinstance(metadata_dict.get("notified_date"), float)
                    and math.isnan(metadata_dict.get('notified_date'))) \
                or metadata_dict.get('notified_date') == 'nan' or metadata_dict.get('notified_date') == '':
            metadata_dict["notified_date"] = format_date_as_odatav4(notified_date)
        else:
            metadata_dict["notified_date"] = format_date_as_odatav4(metadata_dict.get('notified_date'))

        if metadata_dict.get("URL") is None \
                or (isinstance(metadata_dict.get("URL"), float) and math.isnan(metadata_dict.get('URL'))) \
                or metadata_dict.get('URL') == 'nan':
            metadata_dict["URL"] = ""

    except Exception as e:
        app_logger.error(f"An error occurred while generating metadata: {str(e)}")
        metadata_dict["error"] = str(e)

    return metadata_dict


def extract_regulation_content(directory_path):
    """
    Extracts content from text, summarize, and json files in the specified directory of the regulation.

    Args:
        directory_path (str): The path to the directory containing the regulation files.

    Returns:
        tuple: A tuple containing lists of text contents, summarize contents, and json contents of the regulation files.
    """
    txt_contents = []
    pdf_contents = []
    json_contents = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)

            if file_path.endswith('.txt'):
                try:
                    with open(file_path, 'r', encoding="utf-8") as f:
                        txt_content = f.read()
                        txt_content = txt_content.strip()
                        app_logger.info("txt File Parsed")
                        if len(txt_content) > 4:
                            txt_contents.append(txt_content)
                        else:
                            app_logger.info("txt File is Empty")
                except Exception as e:
                    app_logger.error(f"Error parsing txt file {file_path}: {str(e)}")
                    continue

            if file_path.endswith('.json') and not file.startswith('metadata'):
                try:
                    with open(file_path, 'r', encoding="utf-8") as f:
                        json_content = json.load(f)
                        app_logger.info("JSON File Parsed")
                        if len(str(json_content)) > 4:
                            json_contents.append(json_content)
                        else:
                            app_logger.info("JSON File is Empty")
                except Exception as e:
                    app_logger.error(f"Error parsing JSON file {file_path}: {str(e)}")
                    continue

            if file_path.endswith('.pdf'):
                try:
                    pdf_content = parse_pdf_with_path(file_path)
                    if len(pdf_content) > 0:
                        pdf_contents.append(pdf_content)
                except pdfminer.pdfparser.PDFSyntaxError as e:
                    app_logger.error(f"PDF syntax error in file {file_path}: {str(e)}")
                    continue
                except Exception as e:
                    app_logger.error(f"Error parsing PDF file {file_path}: {str(e)}")
                    continue

    return txt_contents, pdf_contents, json_contents



def chunk_regulation(metadata, txt_contents, pdf_contents, json_contents):
    """
    Generates a list of chunks from text, summarize, and json contents with associated metadata.

    Args:
        metadata (Dict): Metadata information including title, notified date, website, keyword, notified country, URL.
        txt_contents (List[str]): List of text contents.
        pdf_contents (List[Dict]): List of dictionaries containing summarize contents.
        json_contents (List[Dict]): List of dictionaries containing json contents.

    Returns:
        chunks (List[Dict]): A list of dictionaries where each dictionary represents a chunk of text or data
                             associated with associated metadata.
    """
    chunks = []
    if len(txt_contents) > 0:
        all_text = "\n\n".join(txt_contents)
        text_parent_child_chunks = split_text_to_chunks(all_text)
        child_chunks_txt = generate_child_chunks(text_parent_child_chunks)
        chunks.extend(child_chunks_txt)

    if len(pdf_contents) > 0:
        for pdf_content_dict in pdf_contents:
            pdf_parent_child_chunks = split_pdf_to_chunks(pdf_content_dict)
            child_chunks_pdf = generate_child_chunks(pdf_parent_child_chunks)
            chunks.extend(child_chunks_pdf)

    if len(json_contents) > 0:
        for table in json_contents:
            table_json = json.dumps(table)
            table_string = "Table: " + table_json
            table_parent_child_chunks = split_text_to_chunks(table_string)
            child_chunks_table = generate_child_chunks(table_parent_child_chunks)
            chunks.extend(child_chunks_table)

    for chunk in chunks:
        chunk["title"] = metadata["title"]
        chunk["date"] = metadata["notified_date"]
        chunk["website"] = metadata["website"]
        chunk["keyword"] = metadata["keyword"]
        chunk["notified_country"] = metadata["notified_country"]
        chunk["url"] = metadata["URL"]
        
    return chunks

def generate_child_chunks(parent_child_chunks: dict) -> list:

    child_chunks = []
    for _, c_chunks in parent_child_chunks.items():
        for c_chunk in c_chunks:
            c_chunk["chunk_vector"] = get_embedding(c_chunk["chunk"])
            child_chunks.append(c_chunk)

    return child_chunks

def ingest_regulation(chunks):
    """
    Ingests provided data chunks and saves them to a JSON file for later inspection.

    Args:
        chunks (List[Dict]): A list of data chunks to ingest.

    Returns:
        None
    """
    with open('chunks_output.json', 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)

    ingest_chunks(chunks)


def create_index_if_not_exists() -> None:
    """
    Ensuring index existence, creating index if necessary.

    Args:
        None

    Returns:
        None
    """
    if not does_index_exists():
        create_index()


def main(target_website_name: str):
    blob_service_client = BlobServiceClient.from_connection_string(BLOB_STORAGE_CONFIG['connection_string'])
    container_client = blob_service_client.get_container_client(container=BLOB_STORAGE_CONFIG['container_name'])
    blobs = container_client.list_blobs()

    create_index_if_not_exists()

    for my_blob in blobs:
        website_name = my_blob.name.split('/')[0]
        if website_name != target_website_name:
            continue

        metadata = {}
        txt_contents = []
        pdf_contents = []
        json_contents = []
        with tempfile.TemporaryDirectory() as temp_dir:
            if my_blob.name.endswith('.zip'):
                keyword = my_blob.name.split('/')[1]
                file_name_with_extension = my_blob.name.split('/')[-1]
                file_name = file_name_with_extension.split('.')[0]
                notified_date = file_name[:10]

                try:
                    datetime.strptime(notified_date, '%Y-%m-%d')
                except ValueError:
                    app_logger.error(f"Invalid date format in file name {file_name}. Skipping this zip file.")
                    continue

                app_logger.info(f"Downloading and extracting {my_blob.name} ...")
                blob_client = blob_service_client.get_blob_client(container=BLOB_STORAGE_CONFIG['container_name'],
                                                                  blob=my_blob.name)
                zip_data = blob_client.download_blob().read()

                zip_path = os.path.join(temp_dir, "my_compressed_zip.zip")
                with open(zip_path, "wb") as fp:
                    fp.write(zip_data)

                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                metadata = get_meta_data(temp_dir, website_name, file_name, keyword, notified_date)
                if check_document_existence_by_title_and_date(metadata["title"].replace("'", "\'"),
                                                              metadata["notified_date"]):
                    app_logger.info("The document is already indexed!")
                    continue
                txt_contents, pdf_contents, json_contents = extract_regulation_content(temp_dir)

        chunks = chunk_regulation(metadata, txt_contents, pdf_contents, json_contents)
        ingest_regulation(chunks)
        app_logger.info(f"Successfully ingested {my_blob.name} ...\n{'-' * 50}")




app = FastAPI()

class SiteRequest(BaseModel):
    website_name: str

@app.post("/process-site/")
def process_site(request: SiteRequest):
    allowed_sites = ["ECHA", "eur_lex", "resmigazete", "all"]
    if request.website_name not in allowed_sites:
        raise HTTPException(status_code=400, detail="Invalid website name")

    if request.website_name == "all":
        for site in allowed_sites[:-1]:
            main(site)
        return {"message": "Processing started for all websites"}
    else:
        main(request.website_name)
        return {"message": f"Processing started for {request.website_name}"}

if __name__ == "__main__":
    # import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)

    main("eur_lex")