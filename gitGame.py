import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QRadioButton, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QButtonGroup, QProgressBar
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

# Quiz data based on your lecture
questions = [
    {
        'question': '1. What is Git primarily used for?',
        'options': [
            'A) Project management',
            'B) Version control system to track changes in files',
            'C) Programming language',
            'D) Operating system'
        ],
        'answer': 'B'
    },
    {
        'question': '2. Which command initializes a new Git repository?',
        'options': [
            'A) git clone',
            'B) git init',
            'C) git commit',
            'D) git push'
        ],
        'answer': 'B'
    },
    {
        'question': '3. What is the correct command to clone a repository using SSH?',
        'options': [
            'A) git clone git@github.com:user/repo.git',
            'B) git clone https://github.com/user/repo.git',
            'C) git init git@github.com:user/repo.git',
            'D) git pull git@github.com:user/repo.git'
        ],
        'answer': 'A'
    },
    {
        'question': '4. Which command stages changes to be committed?',
        'options': [
            'A) git status',
            'B) git commit',
            'C) git add <file>',
            'D) git push'
        ],
        'answer': 'C'
    },
    {
        'question': '5. How do you commit changes with a message?',
        'options': [
            'A) git commit -m "Your commit message"',
            'B) git add "Your commit message"',
            'C) git push "Your commit message"',
            'D) git status -m "Your commit message"'
        ],
        'answer': 'A'
    },
    {
        'question': '6. Which command updates your local repository with changes from the remote repository?',
        'options': [
            'A) git push',
            'B) git pull',
            'C) git fetch',
            'D) git merge'
        ],
        'answer': 'B'
    },
    {
        'question': '7. What command would you use to check the status of your working directory and staging area?',
        'options': [
            'A) git log',
            'B) git status',
            'C) git diff',
            'D) git checkout'
        ],
        'answer': 'B'
    },
    {
        'question': '8. Which of the following is NOT a Git hosting service mentioned in the lecture?',
        'options': [
            'A) GitHub',
            'B) GitLab',
            'C) BitBucket',
            'D) CodePen'
        ],
        'answer': 'D'
    },
    {
        'question': '9. To set your user name and email in Git, which command would you use?',
        'options': [
            'A) git config --global user.name "Your Name"',
            'B) git set user.name "Your Name"',
            'C) git commit --user "Your Name"',
            'D) git init --user "Your Name"'
        ],
        'answer': 'A'
    },
    {
        'question': '10. What is the purpose of "git push"?',
        'options': [
            'A) To update remote refs along with associated objects',
            'B) To fetch from and integrate with another repository',
            'C) To record changes to the repository',
            'D) To create a new branch'
        ],
        'answer': 'A'
    }
]

class QuizGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Git Quiz Game')
        self.score = 0
        self.qn = 0
        self.init_ui()
        self.display_question()
    
    def init_ui(self):
        # Set window icon if desired
        # self.setWindowIcon(QIcon('icon.png'))
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Apply Mint-Y theme styling
        self.setStyleSheet("""
            QWidget {
                background-color: #f2f2f2;
            }
            QLabel {
                color: #3c3c3c;
            }
            QRadioButton {
                padding: 5px;
            }
            QRadioButton::indicator::checked {
                background-color: #87c095;
                border: 1px solid #3c3c3c;
            }
            QRadioButton::indicator {
                border: 1px solid #3c3c3c;
                width: 13px;
                height: 13px;
                border-radius: 7px;
                background: #ffffff;
            }
            QPushButton {
                background-color: #87c095;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #76ab83;
            }
            QProgressBar {
                border: 1px solid #3c3c3c;
                text-align: center;
                color: #3c3c3c;
            }
            QProgressBar::chunk {
                background-color: #87c095;
            }
        """)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(len(questions))
        self.progress_bar.setTextVisible(False)
        self.layout.addWidget(self.progress_bar)

        # Question Label
        self.question_label = QLabel('', self)
        self.question_label.setWordWrap(True)
        self.question_label.setFont(QFont('SansSerif', 14))
        self.layout.addWidget(self.question_label)

        # Options
        self.options_group = QButtonGroup(self)
        self.options_layout = QVBoxLayout()
        self.option_buttons = []
        for i in range(4):
            rb = QRadioButton('', self)
            rb.setFont(QFont('SansSerif', 12))
            self.options_group.addButton(rb)
            self.option_buttons.append(rb)
            self.options_layout.addWidget(rb)
        self.layout.addLayout(self.options_layout)

        # Navigation Buttons
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addStretch()
        self.next_button = QPushButton('Next', self)
        self.next_button.clicked.connect(self.next_question)
        self.buttons_layout.addWidget(self.next_button)
        self.layout.addLayout(self.buttons_layout)
    
    def display_question(self):
        self.progress_bar.setValue(self.qn)
        self.options_group.setExclusive(False)
        for rb in self.option_buttons:
            rb.setChecked(False)
        self.options_group.setExclusive(True)

        question = questions[self.qn]
        self.question_label.setText(question['question'])
        for idx, option in enumerate(question['options']):
            self.option_buttons[idx].setText(option)
            self.option_buttons[idx].setAccessibleName(option[0])  # Store the answer key in AccessibleName

    def next_question(self):
        selected_option = None
        for rb in self.option_buttons:
            if rb.isChecked():
                selected_option = rb.accessibleName()
                break

        if not selected_option:
            QMessageBox.warning(self, 'Warning', 'Please select an option.')
            return

        self.check_answer(selected_option)
        self.qn += 1
        if self.qn == len(questions):
            self.display_result()
            self.close()
        else:
            self.display_question()

    def check_answer(self, selected):
        correct = questions[self.qn]['answer']
        if selected == correct:
            self.score += 1

    def display_result(self):
        result = f"Your final score is {self.score} out of {len(questions)}."
        QMessageBox.information(self, 'Result', result)

def main():
    import os
    os.environ['DISPLAY'] = ':1'  # Use the virtual display
    app = QApplication(sys.argv)
    quiz = QuizGame()
    quiz.resize(600, 400)
    quiz.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

