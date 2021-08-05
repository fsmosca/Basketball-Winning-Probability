import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


DRIVER_PATH = './chromedriver_win32/chromedriver.exe'
options = Options()
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
# options.add_argument('--window-size=1920,1080')


def get_page_title(driver):
    """
    Example title:
    Slovenia v Germany boxscore - Tokyo 2020 Men's Olympic Basketball Tournament - 3 August - FIBA.basketball
    """
    title = driver.title
    teama = title.split(' v')[0]
    teamb = title.split('v ')[1].split(' boxscore')[0]
    return [teama, teamb]


def split_pct(save):
    newsave = []
    for s in save:
        if '\n' in s:
            ms = s.split('\n')[0]
            m = ms.split('/')[0]
            a = ms.split('/')[1]
            pct = float(s.split('\n')[1].split('%')[0])
            newsave.append(int(m))
            newsave.append(int(a))
            newsave.append(round(pct/100, 2))
        else:
            if s != 'Totals':
                newsave.append(int(s))

    return newsave


def get_data(driver, url, urla, urlb, phase='group', category='single'):
    outfn = 'tokyo2021_fiba_oly.csv'

    # Open the main page.
    url = f'{url}#tab=boxscore'
    driver.get(url)

    # Get team names
    teams = get_page_title(driver)
    teama = teams[0]
    teamb = teams[1]
    print(f'teama: {teama}')
    print(f'teamb: {teamb}')

    # Select elements
    xpaths = [urla, urlb]
    data = {teama: [], teamb: []}

    for (t, xp) in zip(teams, xpaths):
        save = []
        for i in range(1, 18):
            tv = driver.find_element_by_xpath(xp + f'/td[{i}]')
            tvtext = tv.text.strip()
            if tvtext == '':
                tvtext = '201'
            save.append(tvtext)

        newsave = split_pct(save)
        data.update({t: newsave})

    for k, v in data.items():
        print(k, v)

    resa, resb = 1, 0
    if data[teama][1] < data[teamb][1]:
        resa = 0
        resb = 1

    # Write output header.
    outfile = Path(outfn)
    if not outfile.is_file():
        with open(outfn, 'a') as w:
            w.write('PHASE,CAT,NAME,OPP,PTS,FGM,FGA,FG%,2PM,2PA,2P%,3PM,3PA,3P%,FTM,FTA,FT%,OREB,DREB,REB,AST,FO,TO,STL,BLK,+/-,EFF,RES\n')

    with open(outfn, 'a') as w:
        w.write(f'{phase},{category},{teama},{teamb},')
        for i in range(1, 24):
            w.write(f'{data[teama][i]},')
        w.write(f'{resa}\n')

        w.write(f'{phase},{category},{teamb},{teama},')
        for i in range(1, 24):
            w.write(f'{data[teamb][i]},')
        w.write(f'{resb}\n')


def main(argv):
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.implicitly_wait(2)  # seconds

    gphase = ['http://www.fiba.basketball/olympics/men/2020/game/2507/Iran-Czech-Republic',
              'http://www.fiba.basketball/olympics/men/2020/game/2507/Germany-Italy',
              'http://www.fiba.basketball/olympics/men/2020/game/2507/Australia-Nigeria',
              'http://www.fiba.basketball/olympics/men/2020/game/2507/France-USA',
              'http://www.fiba.basketball/olympics/men/2020/game/2607/Argentina-Slovenia',
              'http://www.fiba.basketball/olympics/men/2020/game/2607/Japan-Spain',
              'http://www.fiba.basketball/olympics/men/2020/game/2807/Nigeria-Germany',
              'http://www.fiba.basketball/olympics/men/2020/game/2807/USA-Iran',
              'http://www.fiba.basketball/olympics/men/2020/game/2807/Italy-Australia',
              'http://www.fiba.basketball/olympics/men/2020/game/2807/Czech-Republic-France',
              'http://www.fiba.basketball/olympics/men/2020/game/2907/Slovenia-Japan',
              'http://www.fiba.basketball/olympics/men/2020/game/2907/Spain-Argentina',
              'http://www.fiba.basketball/olympics/men/2020/game/3107/Iran-France',
              'http://www.fiba.basketball/olympics/men/2020/game/3107/Italy-Nigeria',
              'http://www.fiba.basketball/olympics/men/2020/game/3107/Australia-Germany',
              'http://www.fiba.basketball/olympics/men/2020/game/3107/USA-Czech-Republic',
              'http://www.fiba.basketball/olympics/men/2020/game/0108/Argentina-Japan',
              'http://www.fiba.basketball/olympics/men/2020/game/0108/Spain-Slovenia'
    ]

    qphase = ['https://www.fiba.basketball/olympics/men/2020/game/0308/Slovenia-Germany',
              'https://www.fiba.basketball/olympics/men/2020/game/0308/Spain-USA',
              'http://www.fiba.basketball/olympics/men/2020/game/0308/Italy-France',
              'http://www.fiba.basketball/olympics/men/2020/game/0308/Australia-Argentina'
    ]

    sfphase = ['http://www.fiba.basketball/olympics/men/2020/game/0508/USA-Australia',
              'http://www.fiba.basketball/olympics/men/2020/game/0508/France-Slovenia'
              ]

    # xpaths to get team summary stats
    urla = '//*[@id="gamepage_boxscore"]/div[2]/div/section[1]/div/table/tfoot/tr[2]'
    urlb = '//*[@id="gamepage_boxscore"]/div[2]/div/section[2]/div/table/tfoot/tr[2]'

    urls = gphase
    # category can be single or average.
    for url in urls:
        time.sleep(5)
        get_data(driver, url, urla, urlb, phase='group', category='single')

    urls = qphase
    for url in urls:
        time.sleep(5)
        get_data(driver, url, urla, urlb, phase='quarter', category='single')

    urls = sfphase
    for url in urls:
        time.sleep(5)
        get_data(driver, url, urla, urlb, phase='semi', category='single')

    driver.quit()


if __name__ == '__main__':
    main(sys.argv[1:])

