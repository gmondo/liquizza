# Liquizza

Liquizza is a quiz app created by ChatGPT and gmondo. 

Test your knowledge, answer questions, and enjoy an interactive quiz experience.

## Features

- Load custom question sets from files.
- Choose the correct answers from multiple options.
- Receive feedback on your performance, including average response time.
- Engaging, educational, and fun!

## Getting Started

1. Connect to https://raw.githack.com/gmondo/liquizza/main/liquizza.html
2. Download a sample and personalize it
3. Upload your personalized sample and start the quiz! 

## File formats

Liquizza support two textual files:

* .csv with the following format:

```
# Comment
Question;Wrong Response 1;Wrong Response 2;...;;Right Response 1;...
```

Please note the void field between wrong and right responses.

* .txt that allows questions on multiple lines with the following format:

```
# Comment
Question 1 on two
lines

Wrong Response 1
...

Right Response 1
...

Question 2
...
```

Here the separator between questions and responses is a void line.

## License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contribution

Contributions are welcome! Feel free to submit pull requests or open issues for any improvements or fixes.

## Contact

For questions or feedback, contact [gmondo](https://github.com/gmondo).

Enjoy the quiz!
