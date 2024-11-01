package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strings"
	"time"

	"github.com/PuerkitoBio/goquery"
)

func randomUserAgent() string {
	return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

func parseArticlePage(articleDict map[string]string) (map[string]string, error) {
	parsedArticles := make(map[string]string)
	for articleName, articleLink := range articleDict {
		req, err := http.NewRequest("GET", articleLink, nil)
		if err != nil {
			return nil, err
		}
		req.Header.Set("User-Agent", randomUserAgent())

		resp, err := http.DefaultClient.Do(req)
		if err != nil {
			return nil, err
		}
		defer resp.Body.Close()

		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			return nil, err
		}

		doc, err := goquery.NewDocumentFromReader(strings.NewReader(string(body)))
		if err != nil {
			return nil, err
		}

		articleContent := doc.Find("div.article-formatted-body").Text()
		parsedArticles[articleName] = articleContent
	}

	return parsedArticles, nil
}

func main() {
	url := "https://habr.com/ru/articles/"
	headers := map[string]string{
		"Accept":     "application/json, text/plain, */*",
		"User-Agent": randomUserAgent(),
	}

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		log.Fatal(err)
	}

	for key, value := range headers {
		req.Header.Set(key, value)
	}

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	doc, err := goquery.NewDocumentFromReader(strings.NewReader(string(body)))
	if err != nil {
		log.Fatal(err)
	}

	articleDict := make(map[string]string)
	doc.Find(".tm-title__link").Each(func(i int, s *goquery.Selection) {
		articleName := s.Find("span").Text()
		articleLink, _ := s.Attr("href")
		articleDict[articleName] = "https://habr.com" + articleLink
	})

	parsedArticles, err := parseArticlePage(articleDict)
	if err != nil {
		log.Fatal(err)
	}

	now := time.Now().Format("2006-01-02")
	filename := fmt.Sprintf("new_go_parsed_articles_%s.json", now)
	data, err := json.MarshalIndent(parsedArticles, "", "  ")
	if err != nil {
		log.Fatal(err)
	}
	err = ioutil.WriteFile(filename, data, 0644)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Articles were successfully parsed")
}

// package main

// import (
// 	"fmt"
// 	"io/ioutil"
// 	"log"
// 	"net/http"
// 	"strings"

// 	"github.com/PuerkitoBio/goquery"
// )

// func parseArticlePage(articleLink string) (string, error) {
// 	// Код для парсинга полной версии статьи
// 	req, err := http.NewRequest("GET", articleLink, nil)
// 	if err != nil {
// 		return "", err
// 	}

// 	resp, err := http.DefaultClient.Do(req)
// 	if err != nil {
// 		return "", err
// 	}
// 	defer resp.Body.Close()

// 	body, err := ioutil.ReadAll(resp.Body)
// 	if err != nil {
// 		return "", err
// 	}

// 	doc, err := goquery.NewDocumentFromReader(strings.NewReader(string(body)))
// 	if err != nil {
// 		return "", err
// 	}

// 	articleContent := doc.Find("div.article-formatted-body").Text()
// 	return articleContent, nil
// }

// func main() {
// 	// URL RSS-файла
// 	url := "https://habr.com/ru/rss/"

// 	// Получить RSS-файл
// 	resp, err := http.Get(url)
// 	if err != nil {
// 		log.Fatal(err)
// 	}
// 	defer resp.Body.Close()

// 	// Парсить RSS-файл
// 	rss, err := rss.Parse(resp.Body)
// 	if err != nil {
// 		log.Fatal(err)
// 	}

// 	// Извлекать необходимую информацию
// 	for _, item := range rss.Items {
// 		articleLink := item.Link
// 		articleContent, err := parseArticlePage(articleLink)
// 		if err != nil {
// 			log.Fatal(err)
// 		}

// 		fmt.Println(articleContent)
// 	}
// }

// -----------------------------------
// package main

// import (
// 	"encoding/json"
// 	"fmt"
// 	"io/ioutil"
// 	"log"
// 	"net/http"
// 	"strings"
// 	"time"

// 	"github.com/PuerkitoBio/goquery"
// )

// func randomUserAgent() string {
// 	res := "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
// 	return res
// 	// userAgents := []string{
// 	// 	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
// 	// 	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
// 	// 	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
// 	// 	// добавьте еще несколько вариантов юзер агентов
// 	// }

// 	// rand.Seed(time.Now().UnixNano())
// 	// return userAgents[rand.Intn(len(userAgents))]
// }

// func main() {
// 	// Set up the URL and headers
// 	url := "https://habr.com/ru/articles/"
// 	headers := map[string]string{
// 		"Accept":     "application/json, text/plain, */*",
// 		"User-Agent": randomUserAgent(),
// 	}

// 	// Create a new HTTP request
// 	req, err := http.NewRequest("GET", url, nil)
// 	if err != nil {
// 		log.Fatal(err)
// 	}

// 	// Set the headers
// 	for key, value := range headers {
// 		req.Header.Set(key, value)
// 	}

// 	// Send the request
// 	resp, err := http.DefaultClient.Do(req)
// 	if err != nil {
// 		log.Fatal(err)
// 	}
// 	defer resp.Body.Close()

// 	// Read the response body
// 	body, err := ioutil.ReadAll(resp.Body)
// 	if err != nil {
// 		log.Fatal(err)
// 	}

// 	// Parse the HTML using goquery
// 	doc, err := goquery.NewDocumentFromReader(strings.NewReader(string(body)))
// 	if err != nil {
// 		log.Fatal(err)
// 	}

// 	// Find all article links
// 	articleDict := make(map[string]string)
// 	doc.Find(".tm-title__link").Each(func(i int, s *goquery.Selection) {
// 		articleName := s.Find("span").Text()
// 		articleLink, _ := s.Attr("href")
// 		articleDict[articleName] = "https://habr.com" + articleLink
// 	})

// 	// Save the article dictionary to a JSON file
// 	now := time.Now().Format("2006-01-02")
// 	filename := fmt.Sprintf("go_articles_%s.json", now)
// 	data, err := json.MarshalIndent(articleDict, "", "  ")
// 	if err != nil {
// 		log.Fatal(err)
// 	}
// 	err = ioutil.WriteFile(filename, data, 0644)
// 	if err != nil {
// 		log.Fatal(err)
// 	}
// 	fmt.Println("Articles were successfully retrieved")
// }
// ---------------------------------------------------
// package main

// import (
// 	"encoding/json"
// 	"fmt"
// 	"io/ioutil"
// 	"log"
// 	"net/http"
// 	"strings"
// 	"time"

// 	"github.com/PuerkitoBio/goquery"
// )

// func main() {
// 	// Set up the URL and headers
// 	url := "https://habr.com/ru/articles/"
// 	headers := map[string]string{
// 		"Accept":     "application/json, text/plain, */*",
// 		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
// 	}

// 	// Send a GET request to the URL
// 	resp, err := http.Get(url)
// 	if err != nil {
// 		log.Fatal(err)
// 	}
// 	defer resp.Body.Close()

// 	// Read the response body
// 	body, err := ioutil.ReadAll(resp.Body)
// 	if err != nil {
// 		log.Fatal(err)
// 	}

// 	// Parse the HTML using goquery
// 	doc, err := goquery.NewDocumentFromReader(strings.NewReader(string(body)))
// 	if err != nil {
// 		log.Fatal(err)
// 	}

// 	// Find all article links
// 	articleDict := make(map[string]string)
// 	doc.Find(".tm-title__link").Each(func(i int, s *goquery.Selection) {
// 		articleName := s.Find("span").Text()
// 		articleLink, _ := s.Attr("href")
// 		articleDict[articleName] = "https://habr.com" + articleLink
// 	})

// 	// Save the article dictionary to a JSON file
// 	now := time.Now().Format("2006-01-02")
// 	filename := fmt.Sprintf("go_articles_%s.json", now)
// 	data, err := json.MarshalIndent(articleDict, "", "  ")
// 	if err != nil {
// 		log.Fatal(err)
// 	}
// 	err = ioutil.WriteFile(filename, data, 0644)
// 	if err != nil {
// 		log.Fatal(err)
// 	}
// 	fmt.Println("Articles were successfully retrieved")
// }
