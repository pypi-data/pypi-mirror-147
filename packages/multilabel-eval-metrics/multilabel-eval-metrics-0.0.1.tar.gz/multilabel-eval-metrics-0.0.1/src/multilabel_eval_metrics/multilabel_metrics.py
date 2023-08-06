import pickle
import os
import numpy as np
import numpy as np
# https://medium.datadriveninvestor.com/a-survey-of-evaluation-metrics-for-multilabel-classification-bb16e8cd41cd

class MultiLabelMetrics:
    def __init__(self,y_true,y_pred):
        self.y_true=y_true
        self.y_pred=y_pred

    def emr(self, y_true, y_pred):
        n = len(y_true)
        row_indicators = np.all(y_true == y_pred, axis=1)  # axis = 1 will check for equality along rows.
        exact_match_count = np.sum(row_indicators)
        return exact_match_count / n

    def one_zero_loss(self, y_true, y_pred):
        n = len(y_true)
        row_indicators = np.logical_not(
            np.all(y_true == y_pred, axis=1))  # axis = 1 will check for equality along rows.
        not_equal_count = np.sum(row_indicators)
        return not_equal_count / n

    def hamming_loss(self, y_true, y_pred):
        """
    	XOR TT for reference -

    	A  B   Output

    	0  0    0
    	0  1    1
    	1  0    1
    	1  1    0
    	"""
        hl_num = np.sum(np.logical_xor(y_true, y_pred))
        hl_den = np.prod(y_true.shape)

        return hl_num / hl_den

    # hl_value = hamming_loss(y_true, y_pred)
    # print(f"Hamming Loss: {hl_value}")

    # Example-Based Accuracy
    def example_based_accuracy(self, y_true, y_pred):
        # compute true positives using the logical AND operator
        numerator = np.sum(np.logical_and(y_true, y_pred), axis=1)

        # compute true_positive + false negatives + false positive using the logical OR operator
        denominator = np.sum(np.logical_or(y_true, y_pred), axis=1)
        instance_accuracy = numerator / denominator

        avg_accuracy = np.mean(instance_accuracy)
        return avg_accuracy

    # ex_based_accuracy = example_based_accuracy(y_true, y_pred)
    # print(f"Example Based Accuracy: {ex_based_accuracy}")
    def example_based_precision(self, y_true, y_pred):
        """
        precision = TP/ (TP + FP)
        """

        # Compute True Positive
        precision_num = np.sum(np.logical_and(y_true, y_pred), axis=1)

        # Total number of pred true labels
        precision_den = np.sum(y_pred, axis=1)

        # precision averaged over all training examples
        avg_precision = np.mean(precision_num / precision_den)

        return avg_precision

    # ex_based_precision = example_based_precision(y_true, y_pred)
    # print(f"Example Based Precision: {ex_based_precision}")

    def label_based_macro_accuracy(self, y_true, y_pred):
        # axis = 0 computes true positives along columns i.e labels
        l_acc_num = np.sum(np.logical_and(y_true, y_pred), axis=0)

        # axis = 0 computes true postive + false positive + false negatives along columns i.e labels
        l_acc_den = np.sum(np.logical_or(y_true, y_pred), axis=0)

        # compute mean accuracy across labels.
        return np.mean(l_acc_num / l_acc_den)

    # lb_macro_acc_val = label_based_macro_accuracy(y_true, y_pred)
    # print(f"Label Based Macro Accuracy: {lb_macro_acc_val}")

    def label_based_macro_precision(self, y_true, y_pred):
        # axis = 0 computes true positive along columns i.e labels
        l_prec_num = np.sum(np.logical_and(y_true, y_pred), axis=0)

        # axis = computes true_positive + false positive along columns i.e labels
        l_prec_den = np.sum(y_pred, axis=0)

        # compute precision per class/label
        l_prec_per_class = l_prec_num / l_prec_den

        # macro precision = average of precsion across labels.
        l_prec = np.mean(l_prec_per_class)
        return l_prec

    # lb_macro_precision_val = label_based_macro_precision(y_true, y_pred)

    # print(f"Label Based Precision: {lb_macro_precision_val}")

    def label_based_macro_recall(self, y_true, y_pred):
        # compute true positive along axis = 0 i.e labels
        l_recall_num = np.sum(np.logical_and(y_true, y_pred), axis=0)

        # compute true positive + false negatives along axis = 0 i.e columns
        l_recall_den = np.sum(y_true, axis=0)

        # compute recall per class/label
        l_recall_per_class = l_recall_num / l_recall_den

        # compute macro averaged recall i.e recall averaged across labels.
        l_recall = np.mean(l_recall_per_class)
        return l_recall

    # lb_macro_recall_val = label_based_macro_recall(y_true, y_pred)
    # print(f"Label Based Recall: {lb_macro_recall_val}")

    def label_based_micro_accuracy(self, y_true, y_pred):
        # sum of all true positives across all examples and labels
        l_acc_num = np.sum(np.logical_and(y_true, y_pred))

        # sum of all tp+fp+fn across all examples and labels.
        l_acc_den = np.sum(np.logical_or(y_true, y_pred))

        # compute mirco averaged accuracy
        return l_acc_num / l_acc_den

    # lb_micro_acc_val = label_based_micro_accuracy(y_true, y_pred)
    # print(f"Label Based Micro Accuracy: {lb_micro_acc_val}")

    #
    def label_based_micro_precision(self, y_true, y_pred):
        # compute sum of true positives (tp) across training examples
        # and labels.
        l_prec_num = np.sum(np.logical_and(y_true, y_pred))

        # compute the sum of tp + fp across training examples and labels
        l_prec_den = np.sum(y_pred)

        # compute micro-averaged precision
        return l_prec_num / l_prec_den

    # lb_micro_prec_val = label_based_micro_precision(y_true, y_pred)
    # print(f"Label Based Micro Precision: {lb_micro_prec_val}")

    # Function for Computing Label Based Micro Averaged Recall
    # for a MultiLabel Classification problem.

    def label_based_micro_recall(self, y_true, y_pred):
        # compute sum of true positives across training examples and labels.
        l_recall_num = np.sum(np.logical_and(y_true, y_pred))
        # compute sum of tp + fn across training examples and labels
        l_recall_den = np.sum(y_true)

        # compute mirco-average recall
        return l_recall_num / l_recall_den

    # lb_micro_recall_val = label_based_micro_recall(y_true, y_pred)
    # print(f"Label Based Micro Recall: {lb_micro_recall_val}")

    def alpha_evaluation_score(self, y_true, y_pred):
        alpha = 1
        beta = 0.25
        gamma = 1

        # compute true positives across training examples and labels
        tp = np.sum(np.logical_and(y_true, y_pred))

        # compute false negatives (Missed Labels) across training examples and labels
        fn = np.sum(np.logical_and(y_true, np.logical_not(y_pred)))

        # compute False Positive across training examples and labels.
        fp = np.sum(np.logical_and(np.logical_not(y_true), y_pred))

        # Compute alpha evaluation score
        alpha_score = (1 - ((beta * fn + gamma * fp) / (tp + fn + fp + 0.00001))) ** alpha

        return alpha_score

    def estimate_metrics(self, show=True, save=False,save_folder="",save_name=""):
        dict_metrics={}
        exact_match_ratio = self.emr(self.y_true, self.y_pred)
        # print("Exact Match Ratio: ", exact_match_ratio)
        dict_metrics["Extract Match Ratio"]=exact_match_ratio

        one_zero_loss = self.one_zero_loss(self.y_true, self.y_pred)
        # print("1/0 Loss: ", one_zero_loss)
        dict_metrics["1/0 Loss"] = one_zero_loss

        hl_value = self.hamming_loss(self.y_true, self.y_pred)
        # print(f"Hamming Loss: {hl_value}")
        dict_metrics["Hamming Loss"] = hl_value

        ex_based_accuracy = self.example_based_accuracy(self.y_true, self.y_pred)
        # print(f"Example Based Accuracy: {ex_based_accuracy}")
        dict_metrics["Example Based Accuracy"] = ex_based_accuracy

        ex_based_precision = self.example_based_precision(self.y_true, self.y_pred)
        # print(f"Example Based Precision: {ex_based_precision}")
        dict_metrics["Example Based Precision"] = ex_based_precision

        lb_macro_acc_val = self.label_based_macro_accuracy(self.y_true, self.y_pred)
        # print(f"Label Based Macro Accuracy: {lb_macro_acc_val}")
        dict_metrics["Label Based Macro Accuracy"] = lb_macro_acc_val

        lb_macro_precision_val = self.label_based_macro_precision(self.y_true, self.y_pred)
        # print(f"Label Based Precision: {lb_macro_precision_val}")
        dict_metrics["Label Based Precision"] = lb_macro_precision_val

        lb_macro_recall_val = self.label_based_macro_recall(self.y_true, self.y_pred)
        # print(f"Label Based Recall: {lb_macro_recall_val}")
        dict_metrics["Label Based Recall"] = lb_macro_recall_val

        lb_micro_acc_val = self.label_based_micro_accuracy(self.y_true, self.y_pred)
        # print(f"Label Based Micro Accuracy: {lb_micro_acc_val}")
        dict_metrics["Label Based Micro Accuracy"] = lb_micro_acc_val

        lb_micro_prec_val = self.label_based_micro_precision(self.y_true, self.y_pred)
        # print(f"Label Based Micro Precision: {lb_micro_prec_val}")
        dict_metrics["Label Based Micro Precision"] = lb_micro_prec_val

        lb_micro_recall_val = self.label_based_micro_recall(self.y_true, self.y_pred)
        # print(f"Label Based Micro Recall: {lb_micro_recall_val}")
        dict_metrics["Label Based Micro Recall"] = lb_micro_recall_val

        alpha_eval_score = self.alpha_evaluation_score(self.y_true, self.y_pred)
        # print(f"α-Evaluation Score: {alpha_eval_score}")
        dict_metrics["α-Evaluation Score"] = alpha_eval_score


        for k in dict_metrics:
            dict_metrics[k]=round(dict_metrics[k],4)

        if show:
            print()
            print("ML-Metrics\tValue")
            for k in dict_metrics:
                print(f"{k}\t{dict_metrics[k]}")
            print()

        if save:
            metric_folder=f"{save_folder}/metrics"
            if not os.path.exists(metric_folder):
                os.mkdir(metric_folder)
            pickle.dump(self.y_true, open(f"{metric_folder}/{save_name}_actual.pickle", 'wb'))
            pickle.dump(self.y_pred, open(f"{metric_folder}/{save_name}_predicted.pickle", 'wb'))
            pickle.dump(dict_metrics,open(f"{metric_folder}/{save_name}_metrics.pickle", 'wb'))

        return dict_metrics
