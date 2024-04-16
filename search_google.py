try:
    from googlesearch import search
except ImportError: 
    print("No module named 'google' found")

def search_google(query):
    num_results = 1  # Bắt đầu với num=1
    filtered_results = []
    while filtered_results == []:  # Lặp cho đến khi có kết quả không phải là video YouTube
        results = search(query, num=num_results, stop=3)  
        for result in results:
            if 'youtube.com' not in result:
                filtered_results.append(result)
        if filtered_results:  
            return filtered_results  
        else:
            num_results += 1  # Tăng số lượng kết quả mỗi lần lặp

# test
# query = "Liệu HCM có mưa vào ngày mai hay không?"
# for result in search_google(query):
#     print(result)