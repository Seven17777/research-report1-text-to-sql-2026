# Research Report 1 — 答辩速记

Yao Qiqi · 26723820

## 一分钟英文介绍

My report studies how execution feedback helps language models with up to 30 billion
parameters detect and correct Text-to-SQL errors. I review ten 2026 studies and
organize them into interactive correction, localized credit assignment, and more
reliable verification. My main conclusion is that successful execution does not
guarantee semantic correctness. A query can return the right result by accident on
one database. We also need to separate gold-answer feedback used in training from
signals available at deployment. I compare matched ablations and decoding budgets,
rather than ranking incompatible headline scores. The accompanying SQLite example
illustrates accidental correctness; it is not a reproduction of the model experiments.

## 性能数字

EX 是预测 SQL 与标准 SQL 在指定数据库上得到相同结果的比例。它不是“没有报错”的比例。
下面不是总排名；模型、提示、数据和候选数量不同。

|论文|可记住的数字|一定要说明|
|---|---|---|
|ReEx-SQL|7B BIRD Dev 63.4% / 65.3%|分别是 greedy / 8次采样投票|
|SQL-Trail|7B BIRD Dev 60.1% / 64.2%|greedy / majority；同文单轮多轮消融56.3→59.3|
|ReSQL|Qwen7B 44.39%→53.78%|整个训练、检索、两轮纠错组合的变化|
|EXPO-SQL|7B 68.5%→71.3%|同文均匀奖励与子句奖励消融；8候选|
|FineStep|4B 66.23%→68.51%|与GRPO相比；Vote@8；+2.28个百分点|
|FINER-SQL|3B 67.73%|每题30候选；大模型教师训练成本另计|
|DPC|7B 46.4%→47.6%|该文BIRD评测；同一5候选池中的SC与DPC|
|Progress-SQL|7B 61.2%→64.3%|单轮RL与完整方法消融；Vote@8|
|SERL-SQL|7B 75.55%|奖励筛选条件；摘要76.56%来自32B，超出本报告范围|
|Counterfactual|错误查询拿满奖励29.5%→16.8%|合成奖励审计；不是模型EX提高；训练未稳定改善|

出处及表号见 `source-audit.csv`。正式报告中保留了完整参考链接。

## 常见问题与回答

**研究问题是什么？**

When does execution feedback improve semantic correctness under a fixed model and
computation budget?

在固定模型和计算预算下，执行反馈何时真正提高语义正确率？

**为什么能执行还会错？**

The database checks whether a query is valid, not whether it matches the user's intent.
Counting orders instead of distinct customers is executable but may answer a different question.

数据库不知道用户意图；统计订单数与统计客户数都能运行。

**十篇论文怎么分类？**

Interactive methods change how the model revises SQL. Credit-assignment methods
change which decisions receive training signals. Verification methods change how
the system checks or selects a candidate.

记住：怎么改、学哪里、怎么验证。部分论文跨类别。

**为什么不直接比较最高分？**

Different studies use different training data, prompts, backbones, candidate counts,
and selectors. A matched ablation provides stronger evidence for a specific mechanism.

优先看同论文消融，不把30候选成绩与单次生成成绩直接排排名。

**Greedy、Vote@8、Pass@8 有什么区别？**

Greedy evaluates one generation. Vote@8 selects among eight candidates by agreement.
Pass@8 asks whether any of the eight is correct, using an oracle for evaluation.
Pass@8 does not show that a deployed selector can identify the correct candidate.

**什么是训练时的 privileged feedback？**

It is information available during training but unavailable when answering a new user
question, such as the gold SQL or a gold-derived clause diagnostic.

训练可以用标准答案奖励，部署不能假装事先知道标准答案。

**为什么30B限制不等于便宜？**

Policy size does not include teacher generation, auxiliary models, training rollouts,
optimizer states, KV cache, or multiple candidates. Total and active MoE parameters
must also be distinguished.

FineStep的30B-A3B总参数是30B、活跃约3B；不能叫3B总模型。

**多纠错几轮一定更好吗？**

No. Revisions can fix wrong answers and corrupt correct ones. The net change depends
on both fix rate and regression rate.

初始准确率a，修复率f，改错率r，净变化是(1−a)f−ar。

**SQLite例子说明什么？**

The predicates score >= 80 and score > 80 return the same count on scores [60,90].
Adding a valid row with score 80 distinguishes them. One-instance agreement is
therefore weaker than semantic equivalence.

**反例数据库是不是证明了正确？**

No finite test suite proves universal equivalence. It can expose specific errors,
but the tests, constraints and reference implementation can themselves be wrong.

**报告最重要的结论是什么？**

Reliable correction requires reliable feedback, a clear oracle boundary, and
budget-matched evaluation. More feedback is not automatically better feedback.

这是跨论文综合判断，不是任何一篇论文的原话。

**你是否复现了十篇论文？**

No. This is a literature survey based on the original papers' reported experiments.
I ran an illustrative SQLite example, not the ten model-training pipelines.

如实回答，不把文献数据说成自己跑的实验。

**未来实验怎么设计？**

Use the same 3B or 7B backbone, prompts, databases and total token/tool budget.
Compare one-shot generation, error-only repair, result-aware repair and a stronger
verifier. Report EX, test-suite agreement, fix/regression rates, cost and multiple seeds.

**论文日期与质量如何处理？**

The report uses formal 2026 publication dates for archival conference papers and
first arXiv release dates for preprints. It labels publication status and treats recent
preprints as provisional evidence, especially the November counterfactual study.

不声称十篇都经过同行评审，也不把2026修订日期当作首次发表日期。

## 关于选题、投入成本和研究设计

**为什么选这个题，为什么有意思？**

It connects AI with data engineering. The interesting problem is that an executable
query can return a plausible but incorrect answer, and even match a reference result
by accident on one database. I want to understand which feedback improves meaning,
not just whether the query runs.

它直接联系AI与数据工程。最有意思的是“能执行”和“语义正确”之间的差距。

**怎样判断投入成本合理？**

Compare reliability at the same cost, or cost at the same reliability. Count training
compute, teacher calls, generated tokens, database calls and latency. A higher score
with many more candidates does not by itself establish good value. This report
proposes that evaluation; it does not claim a measured financial return.

同成本更准确，或同准确率更省成本。没有实际项目预算时，不编造资金回报。

**参数怎么选？**

Model size and hyperparameters are different. Start with 3B and 7B policies under the
30B limit. Choose learning rate, temperature, candidate count and turn limit on a
validation set, then freeze them for the test set. The model weights themselves are
learned during training rather than selected one by one.

30B是上限，不是必须达到的规模。候选数和轮次同时改变效果与成本。

**这些与本报告的设计有什么联系？**

Section 10 holds the backbone, prompts, databases and resource budget fixed. It
compares one-shot generation, error-only repair, result-aware repair, voting and
counterexample verification. This separates the value of informative feedback from
the value of simply making more attempts.

第10节就是围绕“反馈是否值得其成本”设计控制实验；第8节SQLite例子实际运行过，
十个大模型训练流程没有复现。
