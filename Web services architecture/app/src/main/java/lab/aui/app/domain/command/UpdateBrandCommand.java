package lab.aui.app.domain.command;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class UpdateBrandCommand {
    private String name;
    private String country;
}