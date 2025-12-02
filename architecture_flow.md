# Multi-Agent Debate System (MAS) - Architecture Flow (Dark Mode)

```mermaid
%% 设置深色主题
%% GitHub 支持部分 themeVariables，在黑底网页更清晰
%% background: 节点背景色，fill: 节点填充，stroke: 边框，textColor: 文本颜色
%% arrowColor: 箭头颜色
%% 注意：GitHub 有些属性默认支持，深色模式会继承 background

%% 主题自定义
%% GitHub 渲染时可使用 classDef 控制节点颜色
flowchart TD
    %% 用户输入
    A[User Input] --> B[Orchestrator / Debate Manager]
    
    %% 智能体
    B --> C1[Pro Debate Agent]
    B --> C2[Con Debate Agent]
    
    %% 辩论记录
    C1 --> D[Debate History]
    C2 --> D[Debate History]
    
    %% 裁判评估
    D --> E[Judge Agent]
    
    %% 输出最终结果
    E --> F[Final Output]

    %% 节点样式
    classDef module fill:#222222,stroke:#ffffff,stroke-width:2px,color:#ffffff;
    class A,B,C1,C2,D,E,F module;
