import requests
import argparse
import json
import datetime
import os
import frontmatter

def get_all_questions():
    r = requests.get('https://leetcode-cn.com/api/problems/all/')
    r.raise_for_status()
    return r.json()

def get_title_slug(question_id):
    all_problems = get_all_questions()
    question_id = str(question_id)
    def func(question):
        return question['stat']['frontend_question_id'] == question_id
    res = list(filter(func, all_problems['stat_status_pairs']))
    assert len(res) == 1
    # print(res[0])
    return res[0]['stat']['question__title_slug']

def get_question_info(title_slug):
    data = {}
    data['query'] = """query questionData($titleSlug: String!) {  
        question(titleSlug: $titleSlug) {    
            questionId
            title    
            titleSlug    
            translatedTitle    
            difficulty    
            langToValidPlayground    
            topicTags {      
                name      
                slug      
                translatedName      
                __typename    
            }   
            stats    
        }
    }"""
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=USxhiUtZhWDk3HRbMjsVehxFVmfcYWjBsYzyOgNezcyzkW2BcxuN0JBBU2w4oSRB'
    }
    data['variables'] = {'titleSlug': title_slug}
    url = 'https://leetcode-cn.com/graphql'

    r = requests.request("POST", url, headers=headers, data = json.dumps(data))
    r.raise_for_status()
    return r.json()['data']['question']

def get_question(question_id):
    title_slug = get_title_slug(question_id)
    question = get_question_info(title_slug)
    data = {}
    data['title'] = str(question_id) + '. ' + question['title']
    data['date'] = datetime.datetime.now().isoformat()
    data['tags'] = [tag['name'] for tag in question['topicTags']] + ['LeetCode']
    data['categories'] = ['LeetCode']
    url = 'https://leetcode-cn.com/problems/'
    content = '今天的题目是[%s](%s)。\n\n' % (data['title'], url + title_slug) 
    return title_slug, frontmatter.Post(content, **data)



def main():
    parser = argparse.ArgumentParser(description='leetcode blog generator')
    parser.add_argument('question_id', type=int, metavar='question_id', 
            help='leetcode problem id')
    parser.add_argument('output_dir', type=str, metavar='output_dir', help='output dir')
    args = parser.parse_args()
    title_slug, data = get_question(args.question_id)
    path = os.path.join(args.output_dir, title_slug + '.md')
    print(path)
    print(frontmatter.dumps(data))
    with open(path, 'w') as f:
        f.write(frontmatter.dumps(data))
    

if __name__ == "__main__":
	main()
