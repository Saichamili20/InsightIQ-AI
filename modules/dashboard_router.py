from modules.dataset_detector import detect_dataset




def generate_dashboard(df):

    dataset_type = detect_dataset(df)

   