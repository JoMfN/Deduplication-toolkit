import os

def select_file_to_keep(file_list, criterion='oldest'):
    if criterion == 'oldest':
        return sorted(file_list, key=lambda f: os.path.getctime(f))[0]
    elif criterion == 'largest':
        return sorted(file_list, key=lambda f: os.path.getsize(f), reverse=True)[0]
    elif criterion == 'shortest_name':
        return sorted(file_list, key=lambda f: len(os.path.basename(f)))[0]
    return file_list[0]  # fallback
