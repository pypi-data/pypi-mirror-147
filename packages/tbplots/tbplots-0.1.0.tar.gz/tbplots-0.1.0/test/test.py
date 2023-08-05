
import tbplots

if __name__ == "__main__":
    iFilter=["LR1e5","LR5e5","LR1e4"]
    tbplots.PlotTensorflowData(path=".",gFilter="4R_PPO",iFilter=iFilter,
        metric="Env Results/WinRate",saveName="LR_HP_Median",
        title="4 Rooms PPO Learning Rate Exp",
        xlabel="Episode",ylabel="Win Rate"
        )
    tbplots.PlotTensorflowData(path=".",gFilter="4R_PPO",iFilter=iFilter,
        metric="Env Results/WinRate",saveName="LR_HP_Mean",
        title="4 Rooms PPO Learning Rate Exp",
        xlabel="Episode",ylabel="Win Rate",plotStyle="Confidence",
        )
