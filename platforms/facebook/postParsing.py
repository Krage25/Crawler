import requests
import traceback

def callParserAPI(input_text):
    # input_text = "Log in Forgotten account? Video More Home Live Reels Shows Explore 0:03 / 8:19 Legendary SP Balasubrahmanyam's live performance in multiple languages at SIIMA Awards | #SPBLivesOn Like Comment Share 111K · 1.7K comments · 2.6M views SIIMA 4 June 2023 · Follow Legendary SP Balasubrahmanyam's live performance in multiple languages at SIIMA Awards.… See more Comments Most relevant Savitha Lokesh Love you SPB Sir forever love you from karnataka people is forever 1y 3 Padmavathi Rao Ever green singer our balu sir 1y 17 View all 2 replies View more comments 2 of 1,679 Related reels SIIMA 110K SIIMA 48K SIIMA 34K SIIMA 39K SIIMA 9.4K SIIMA 16K SIIMA 24K SIIMA 6.9K SIIMA 19K SIIMA 20K SIIMA 17K SIIMA 40K Related videos 4:17 Mohan Babu Relives His Fondest Memory of Rama Naidu Garu with Rana Daggubati. SIIMA 1.4K views · 3d ago 3:12 Rajendra Prasad's Heartfelt Gratitude to Allu Arjun: A Touching Moment You Can't Miss. SIIMA 11.1K views · 3d ago 4:03 Shruti Haasan's Glowing Reaction to Samantha's Unstoppable Energy at SIIMA! SIIMA 17.5K views · 3d ago 3:35 DSP's Hilarious Reaction to Srikanth's Epic Moments with Thaman | SIIMA SIIMA 16K views · 3d ago 6:34 Jailer 2 Director Nelson Dilip Kumar & Yogi Babu Delights the Stage. SIIMA 33.5K views · 5d ago 6:08 Laxmi Raai was spellbound by Yash's Unforgettable Speech at the SIIMA Awards SIIMA 183.3K views · 5d ago 0:39 Marking the 102nd birth anniversary of the legendary Nandamuri Taraka Rama Rao (NTR), his grandsons Jr. NTR and Nandamuri Kalyan Ram paid a heartfelt tribute at NTR Ghat in Hyderabad. 🙏💐 #NTRJayanthi #NandamuriLegacy #JrNTR #KalyanRam #ManOfMasses #NTRGhat #TeluguPride #LegendLivesOn #NTR102ndAnniversary #siima SIIMA 163.7K views · 28 May at 07:59 3:05 Producer Allu Arvind Reveals Surprising Truth Behind Paradise's Director Srikanth Odela. SIIMA 46.4K views · 22 May at 17:29 4:09 Nandita Swetha Names Her Favorite Actor! | Watch Kushboo's Hilarious Reaction to Parvathi Thiruvothu. SIIMA 26.5K views · 20 May at 12:55 Pages Interest TV & film TV/Film award SIIMA Videos Legendary SP Balasubrahmanyam's live performance in multiple languages at SIIMA Awards | #SPBLivesOn Home Live Explore Shows Related pages Behindwoods Media/news company 14M followers English Partner Telugu Education 15K followers Red FM Telugu Broadcasting & media production company 1.1M followers JAIN Center for Global Studies Education website 4.8K followers ZEE5 Tamil Entertainment website 1.5M followers ETV Win Entertainment website 1.4M followers Privacy · Terms · Advertising · Ad choices · Cookies · More · Meta © 2025 See more on Facebook Email address or phone number Password Log in Forgotten password? or Create new account." 
    try:
        url = "http://15.206.70.131:5006/agents/media-info-extract" 

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "input_text": input_text 
        }

        response = requests.post(url, json=payload, headers=headers)

        response.raise_for_status()
        print(response)
        return response.json()  

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}