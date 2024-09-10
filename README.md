# Accuracy comparison of random forest and hybrid neural network models for the classification of text into Keirsey model personality types

This repository is for a research paper presented at the XXI "A Step Into Science" Students Conference at the Petnica Science Center in December 2022

 * See [Usage](#usage) for guidance on how to use this repository.
 * See [Examples](#examples) for examples of the results.

# Abstract

On the (MBTI) Myers-Briggs Personality Type Dataset preprocessing was done using the spaCy library, after which the data was classified using random forest and hybrid neural network models (CNN+LSTM). Before training the hybrid model, word embedding was done using a pre-trained tok2vec tool from spaCy. For reference, a hybrid neural network model which used a tensorflow word embedding layer instead of the spaCy layer was used. The random forest model had a maximum average f1-score of 70% with 10000 estimators, and a minimum average f1-score of 57% with 100 estimators. The hybrid model with spaCy word embedding had a maximum average f1-score of 65%, and the reference model had a maximum average f1-score of 75%. In testing it was shown that the hybrid model was more accurate and that the pre-trained spaCy word embedding layer wasn't adequate for usage on posts which contain a lot of internet jargon.
# Paper

The full paper is written in Serbian and was presented at the XXI "A Step Into Science" Students Conference at the Petnica Science Center in December 2022

It was also presented at the IEEESTEC 15th Student Projects Conference in November 2023 <br>and published in the proceedings of papers - p. 159-162 ISBN 978-86-6125-257-0.

[Link to paper](https://ieee.elfak.ni.ac.rs/wp-content/uploads/2022/11/2022.pdf#page=167)

# Examples

Here are some select examples of the results.

<table>
    <tbody>
        <tr>
            <td align="center">
                <img src="evaluation/spojeni_reciVektori/nospaCy_wholeset_confusion.png" alt="Neural Network Confusion Matrix" style="width:100%">
            </td>
            <td align="center">
                <img src="evaluation/randomForest/confusionMatrix.png" alt="Random Forest Confusion Matrix" style="width:100%">
            </td align="center">
        </tr>
        <tr>
            <td align="center">Confusion matrix for the reference model <br>(hybrid neural network)</td>
            <td align="center">Confusion matrix for the random forest model</td>
        </tr>
    </tbody>
<table>

# Usage

W.I.P.
