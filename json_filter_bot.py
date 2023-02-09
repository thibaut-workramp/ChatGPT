import argparse
import json

from utils import set_logging_level
from base_task_solver_bot import BaseTaskSolverBot


class JsonFilterBot(BaseTaskSolverBot):
    """
    Bot specialized on json filter generation, given a nl filter query about the  dataset
    """
    all_question_type = [
        "text_answer", "multiple_choice", "matching"
    ]

    def build_task_description(self, space_functions=None):
        task_description = f"""\
We consider the following 'questions' dataset schema, with its fields description:

type (string) The type of the space Unique possible values are:  "text_answer", "multiple_choice", "matching"
question (string) The question to ask
choices (list of object): The list of choices for the question (only for multiple_choice questions) where at least one choice is the correct and at least one is incorrect. All choices must be different.
answer (string) The answer to the question (only for text_answer questions)
matching (list) The list of matching pairs (only for matching questions) make sure to not repeat the same label in the matching set we should have around 4 matching sets all labels must be different, it can not have the same label matching different values

Given a natural language input return three questions: a text answer question, a multiple choice choice question and a matching question .\
"""
        return task_description
    examples = (
        {
            "input": "One of the top tourist destinations in the United States, San Francisco is known for its steep rolling hills and eclectic mix of architecture across varied neighborhoods, as well as its cool summers, fog, and landmarks, including the Golden Gate Bridge, cable cars, Alcatraz, and Chinatown and Mission districts.[47] The city is home to a number of educational and cultural institutions, such as the University of California, San Francisco, the University of San Francisco, San Francisco State University, the San Francisco Conservatory of Music, the de Young Museum, the San Francisco Museum of Modern Art, the San Francisco Symphony, the San Francisco Ballet, the San Francisco Opera, the SFJAZZ Center, and the California Academy of Sciences. Two professional sports teams, MLB\'s San Francisco Giants, and the NBA\'s Golden State Warriors, all play their home games within San Francisco proper. Transport to, from, and within San Francisco is also among the most robust in the nation, with a main international airport flying to over 125 destinations and a light rail and bus network in tandem with the BART and Caltrain systems connecting nearly every part of San Francisco with the wider region.",
            "output": {
                'questions': {
                    'text_answer': {
                      'question': 'What is the name of the city?',
                      'answer': 'San Francisco',
                    }, 
                    'multiple_choice': {
                      'question': 'How are the summer in San Francisco?',
                      'choices': ['cool','warm','hot','cold']
                    },
                    'matching': {
                      'question': 'Match the following',
                      'matching': [['San Francisco Giants','MLB'], ['Golden State Warriors','NBA'], ['Summers in San Francisco','cool']]
                    }
                }
            }
        }, {
            "input": "Lincoln was born into poverty in a log cabin in Kentucky and was raised on the frontier, primarily in Indiana. He was self-educated and became a lawyer, Whig Party leader, Illinois state legislator, and U.S. Congressman from Illinois. In 1849, he returned to his successful law practice in central Illinois. In 1854, he was angered by the Kansas–Nebraska Act, which opened the territories to slavery, and he re-entered politics. He soon became a leader of the new Republican Party. He reached a national audience in the 1858 Senate campaign debates against Stephen A. Douglas. Lincoln ran for president in 1860, sweeping the North to gain victory. Pro-slavery elements in the South viewed his election as a threat to slavery, and Southern states began seceding from the nation. During this time, the newly formed Confederate States of America began seizing federal military bases in the south. Just over one month after Lincoln assumed the presidency, the Confederate States attacked Fort Sumter, a U.S. fort in South Carolina. Following the bombardment, Lincoln mobilized forces to suppress the rebellion and restore the union.",
            "output": {
                'questions': {
                    'text_answer': {
                      'question': 'What was Lincoln\'s profession?',
                      'answer': 'lawyer',
                    },
                    'multiple_choice': {
                      'question': 'Where was Lincoln born?',
                      'choices': ['Kentucky','Indiana','Illinois','California']
                    },
                    'matching': {
                      'question': 'Match the following',
                      'matching': [['Lincoln-Douglas debates','Stephen A. Douglas'],['Lincoln\'s assassination','John Wilkes Booth'],['Lincoln\'s Gettysburg Address','Emancipation Proclamation']]
                    }
                }
            }
        }, {
            "input": "Bitcoin (abbreviation: BTC[a] or XBT[b]; sign: ₿) is a protocol which implements a highly available, public, and decentralized ledger. In order to update the ledger, a user must prove they control an entry in the ledger. The protocol specifies that the entry indicates an amount of a token, bitcoin with a minuscule b. The user can update the ledger, assigning some of their bitcoin to another entry in the ledger. Because the token has characteristics of money, it can be thought of as a digital currency.[10] Bitcoin transactions are verified by network nodes through cryptography and recorded in a public distributed ledger called a blockchain. The cryptocurrency was invented in 2008 by an unknown person or group of people using the name Satoshi Nakamoto.[11] The currency began use in 2009,[12] when its implementation was released as open-source software.[7]: ch. 1  The word bitcoin was defined in a white paper published on October 31, 2008.[3][13] It is a compound of the words bit and coin.[14] Bitcoin is legal in seven of the top ten world economies by GDP in 2022.[15][16] The Library of Congress reports that, as of November 2021, nine countries have fully banned bitcoin use, while a further forty-two have implicitly banned it.[17] A few governments have used bitcoin in some capacity. El Salvador has adopted Bitcoin as legal tender, although use by merchants remains low. Ukraine has accepted cryptocurrency donations to fund the resistance to the 2022 Russian invasion. Iran has used bitcoin to bypass sanctions. In the United States, there is no intention to ban Bitcoin.[18] Bitcoin has been described as an economic bubble by at least eight recipients of the Nobel Memorial Prize in Economic Sciences.[19] The environmental impact of bitcoin is worth noting.[20] Its proof-of-work algorithm for bitcoin mining is designed to be computationally difficult, which requires the consumption of increasing quantities of electricity, the generation of which has contributed to climate change.[21][22] According to the University of Cambridge, bitcoin has emitted an estimated 200 million metric tonnes of carbon dioxide since its launch, [23] or about 0.04% of all carbon dioxide released since 2009.[24] Bitcoin miners have an economic incentive to use the cheapest forms of energy.[25][26] Renewable energy is the cheapest form of energy over time,[27] so it is in a Bitcoin miners economic interest to use the cheaper renewable energy when possible.[28] For instance, the UNESCO World Heritage Site, Virunga National Park, in eastern Congo, Africa pays for its operations, using a profitable Bitcoin mining operation powered by the Parks hydroelectric plant.[29] Oil and gas giant Exxon mines Bitcoin using the natural gas flared by oil mining operations to generate their electricity.[30] Mining Bitcoin this way makes use of an otherwise monumental waste of a valuable natural resource.[31] Still other miners reduce their overall energy bill by using the heat generated by their computers to heat their homes,[32] or hot tubs.",
            "output": {
                'questions': {
                    'text_answer': {
                      'question': 'What was the name of the person who invented Bitcoin?',
                      'answer': 'Satoshi Nakamoto',
                    },
                    'multiple_choice': {
                      'question': 'What is the abbreviation for Bitcoin?',
                      'choices': ['BTC','XBT','₿','B']
                    },
                    'matching': {
                      'question': 'Match the following',
                      'matching': [['Bitcoin mining','computational difficulty'],['Bitcoin\'s environmental impact','climate change'],['Bitcoin\'s legal status','El Salvador']]
                    }
                }
            }
        }
    )

    @classmethod
    def encode_example_output(cls, example_output):
        encoded_example_output = json.dumps(example_output, indent=None)
        return encoded_example_output

    @classmethod
    def decode_output(cls, output):
        decoded_output = json.loads(output)
        return decoded_output


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_level', type=str, default='info', help="Must be in ('info', 'error', 'debug')")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    log_level = args.log_level
    set_logging_level(log_level=log_level)

    JsonFilterBot().from_standard_input()


if __name__ == '__main__':
    main()
