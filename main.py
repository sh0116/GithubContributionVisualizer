import requests
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from PIL import Image, ImageDraw, ImageFont, ImageColor
import io, json, requests
import matplotlib.patches as patches
from flask import Flask, send_file, abort

# You can download a TTF font file and use it
font = ImageFont.truetype("font/NotoSans-Regular.ttf", 25)

# Define a custom color map similar to GitHub's contributions graph
cmap = ListedColormap(['#ebedf0', '#c6e48b', '#7bc96f', '#239a3b', '#196127'])

# Define a list of weekday names
weekday_names = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

def custom_color_map(value):
    if value <= 7:
        color = '#ebedf0'
    elif value <= 30:
        color = '#c6e48b'
    elif value <= 100:
        color = '#7bc96f'
    elif value <= 180:
        color = '#239a3b'
    else:
        color = '#196127'
    return color

def draw_contribution_heatmap(data):
    # Convert data to DataFrame
    df = pd.DataFrame(data, columns=['date', 'count'])
    df.set_index('date', inplace=True)

    # Add weekday and week number columns
    df['weekday'] = (df.index.weekday+1)%7
    df['week'] = (df.index - df.index[0]).days // 7
    pivot_table = df.pivot(index='weekday', columns='week', values='count')

    # Draw a heatmap


    # Compute the number of consecutive days with commits until the most recent commit
    df.sort_values('date', inplace=True)
    consecutive_days = 0
    for i in df['count'][::-1]:
        if i > 0: consecutive_days += 1
        else: break

    print(f"Consecutive days with commits until the most recent commit: {consecutive_days}")
    fig, ax = plt.subplots(figsize=(20, 3))
    sns.heatmap(pivot_table, cmap=cmap, linewidths=.5, cbar=False, xticklabels=False, yticklabels=weekday_names, ax=ax)
    #plt.title(f"Consecutive commit dates: {consecutive_days}")
    plt.yticks(rotation=0)
    ax.set_xlabel('') 
    ax.set_ylabel('') 
    #plt.show()
    #plt.imsave('contribution.png')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return Image.open(buf), consecutive_days

def get_contribution_data(user):
    # Get HTML of the page
    r = requests.get(f'https://github.com/{user}')
    soup = BeautifulSoup(r.text, 'html.parser')

    # Find the contribution data
    contributions = soup.find_all('td', {'class': 'ContributionCalendar-day'})

    # Get contribution data
    data = []
    for td in contributions:
        date = datetime.strptime(td.get('data-date'), '%Y-%m-%d')
        count = int(td.get('data-level'))  # 'data-count' has been replaced by 'data-level'
        data.append((date, count))

    return data

def crop_to_circle(image):
    # 크기를 가져오고, 정사각형 크기로 조정
    size = (min(image.size),)*2
    image = image.resize(size, Image.LANCZOS)

    # 원형 마스크를 만듭니다
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)

    # 원형 마스크를 적용하고 테두리를 추가합니다
    result = Image.new('RGB', size, "white")  # 배경색을 흰색으로 설정
    result.paste(image, mask=mask)
    draw_result = ImageDraw.Draw(result)
    draw_result.ellipse((0, 0) + size, outline="#c6e48b", width=10)
    
    return result

def get_user_info(user):
    r = requests.get(f'https://api.github.com/users/{user}')
    data = json.loads(r.text)
    return data

def get_profile_image(user_info):
    response = requests.get(user_info['avatar_url'])
    img = Image.open(io.BytesIO(response.content))
    return img.resize((300, 300))

def draw_color_legend():
    img_legend = Image.new('RGB', (300, 150), 'white')
    d = ImageDraw.Draw(img_legend)
    font = ImageFont.truetype("font/NotoSans-Regular.ttf", 20)

    day_ranges = [7, 30, 100, 180, 365]
    for i, days in enumerate(day_ranges):
        color = custom_color_map(days)
        d.rectangle([(10, i*30), (40, i*30+20)], fill=ImageColor.getrgb(color))
        d.text((50, i*30), f'{days} days', fill='black', font=font)

    return img_legend

def draw_user_info(user_info, contribution_img, consecutive_days):
    img_width = contribution_img.width
    img_height = contribution_img.height + 350  # Add extra space for user info and image

    # Create a new image with white background
    img = Image.new('RGB', (img_width, img_height), 'white')
    d = ImageDraw.Draw(img)

    # Draw user info with the selected font
    input_text = f"{user_info['name']}"
    d.text((600,100), input_text, fill='black', font=ImageFont.truetype("font/NotoSans-Bold.ttf", 40))

    input_text = f"UserID: {user_info['login']}\nProfile: {user_info['html_url']}\nRepos: {user_info['public_repos']}"
    d.text((600,150), input_text, fill='black', font=ImageFont.truetype("font/NotoSans-Regular.ttf", 25))

    # Get user's profile image
    profile_img = crop_to_circle(get_profile_image(user_info))
    img.paste(profile_img, (250, 50))

    # Draw consecutive days circle
    fig, ax = plt.subplots(figsize=(4,4))
    circle = patches.Circle((0.5, 0.5), 0.4, color=custom_color_map(consecutive_days))
    ax.add_patch(circle)
    plt.text(0.5, 0.5, str(consecutive_days), ha='center', va='center', fontsize=28, color='white')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.gca().axis('off')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Load this into an image
    circle_img = Image.open(buf)
    img.paste(circle_img, (1250, 25))  # Update this position to place the circle near the profile picture

    # Paste the contribution graph
    img.paste(contribution_img, (0, 350))

    color_legend = draw_color_legend()
    img.paste(color_legend, (1650, 200))  # Update this position to place the color legend near the profile picture

    return img

'''
# 사용자 이름 입력 (예: sh0116)
user = 'sh0116'
contribution_data = get_contribution_data(user)
contribution_img, consecutive_days = draw_contribution_heatmap(contribution_data)

# Get user info and draw it on the image
user_info = get_user_info(user)
img = draw_user_info(user_info, contribution_img, consecutive_days)

# Save the final image
img.save('final_output.png')

'''



# 이전에 제공한 코드는 여기에...

app = Flask(__name__)

@app.route('/contribution/<user>/<int:width>x<int:height>', methods=['GET'])
def get_contribution_image(user, width, height):
    user = user
    contribution_data = get_contribution_data(user)
    contribution_img, consecutive_days = draw_contribution_heatmap(contribution_data)
    user_info = get_user_info(user)
    img = draw_user_info(user_info, contribution_img, consecutive_days)
    
    # 이미지 크기 변경
    img = img.resize((width, height))
    
    byte_io = io.BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)
    
    return send_file(byte_io, mimetype='image/png')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)