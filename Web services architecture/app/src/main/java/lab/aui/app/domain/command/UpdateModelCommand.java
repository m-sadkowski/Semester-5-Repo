package lab.aui.app.domain.command;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class UpdateModelCommand {
    private String name;
    private int year;
    private double engine;
}